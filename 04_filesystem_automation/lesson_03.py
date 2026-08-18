import argparse
import shutil

from collections import Counter
from pathlib import Path
from typing import TypedDict


TEST_ROOT = Path(
    "04_filesystem_automation/batch_test"
)

class CopyPlanItem(TypedDict):
    source: Path
    destination: Path
    action: str


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Safely copy matching files."
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without copying files.",
    )

    return parser.parse_args()

def find_matching_files(
    source_folder: Path,
    extensions: set[str],
) -> list[Path]:
    matching_files: list[Path] = []

    for item in source_folder.iterdir():
        if not item.is_file():
            continue

        if item.suffix.lower() not in extensions:
            continue

        matching_files.append(item)

    return sorted(matching_files)

def build_copy_plan(
    files: list[Path],
    destination_folder: Path,
) -> list[CopyPlanItem]:
    plan: list[CopyPlanItem] = []

    for source in files:
        destination = (
            destination_folder / source.name
        )

        if destination.exists():
            action = "SKIP"
        else:
            action = "COPY"

        plan.append(
            {
                "source": source,
                "destination": destination,
                "action": action,
            }
        )

    return plan

def print_plan(
    plan: list[CopyPlanItem],
) -> None:
    print("\n--- Copy Plan ---")

    for item in plan:
        print(
            f"[{item['action']}] "
            f"{item['source'].name} "
            f"-> {item['destination']}"
        )

def execute_copy_plan(
    plan: list[CopyPlanItem],
) -> Counter[str]:
    results: Counter[str] = Counter()

    for item in plan:
        source = item["source"]
        destination = item["destination"]

        if not source.is_file():
            results["Skipped"] += 1
            continue

        if destination.exists():
            results["Skipped"] += 1
            continue

        try:
            destination.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            shutil.copy2(
                source,
                destination,
            )

            results["Copied"] += 1

        except OSError:
            results["Failed"] += 1

    return results

def print_summary(
    results: Counter[str],
) -> None:
    separator = "=" * 40

    print(f"\n{separator}")
    print("Batch Copy Summary")
    print(separator)
    print(f"{'Copied:':<15} {results['Copied']}")
    print(f"{'Skipped:':<15} {results['Skipped']}")
    print(f"{'Failed:':<15} {results['Failed']}")
    print(separator)

def main() -> None:
    args = parse_arguments()

    source_folder = (
        TEST_ROOT / "source"
    )

    destination_folder = (
        TEST_ROOT / "destination"
    )

    extensions = {
        ".txt",
        ".pdf",
    }

    files = find_matching_files(
        source_folder,
        extensions,
    )

    plan = build_copy_plan(
        files,
        destination_folder,
    )

    print(f"Dry run: {args.dry_run}")

    print_plan(plan)

    if args.dry_run:
        print("\nDry run enabled. No files were changed.")
        return

    results = execute_copy_plan(plan)

    print_summary(results)



if __name__ == "__main__":
    main()