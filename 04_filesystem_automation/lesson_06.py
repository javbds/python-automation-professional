import argparse
import shutil
import logging

from collections import Counter
from pathlib import Path
from typing import TypedDict


TEST_ROOT = Path(
    "04_filesystem_automation/batch_test"
)

LOG_FILE = TEST_ROOT / "batch_copy.log"



class CopyPlanItem(TypedDict):
    source: Path
    destination: Path
    action: str

def configure_logging() -> None:
    LOG_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format=(
            "%(asctime)s | "
            "%(levelname)s | "
            "%(message)s"
        ),
    )

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
            destination = get_unique_path(destination)

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

        logging.info(
            "%s planned: %s -> %s",
            item["action"],
            item["source"],
            item["destination"],

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

            logging.warning(
                "Skipped missing or invalid source: %s",
                source,
            )

            continue

        if destination.exists():
            results["Skipped"] += 1

            logging.warning(
                "Skipped because destination already exists: %s",
                destination,
            )
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

            if (
                destination.is_file()
                and source.stat().st_size 
                == destination.stat().st_size
            ):
                results["Copied"] += 1

                logging.info(
                    "Copied and verified: %s -> %s",
                    source,
                    destination,
                )
            else:
                results["Failed"] += 1

                logging.error(
                    "Copy verification failed: %s -> %s",
                    source,
                    destination,
                )

        except OSError as error:
            results["Failed"] += 1

            logging.error(
                "Copy failed: %s -> %s | %s",
                source,
                destination,
                error,
            )

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

def get_unique_path(destination: Path) -> Path:
    """Return a destination path that does not already exist."""

    if not destination.exists():
        return destination

    counter = 1

    while True:
        candidate = destination.with_name(
            f"{destination.stem}_{counter}{destination.suffix}"
        )

        if not candidate.exists():
            return candidate

        counter += 1

def main() -> None:
    configure_logging()

    args = parse_arguments()

    logging.info(
        "Batch copy started. Dry run: %s",
        args.dry_run
    )

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

        logging.info(
            "Dry run completed. No files were changed."
        )

        return

    results = execute_copy_plan(plan)

    print_summary(results)

    logging.info(
        "Batch copy completed. Copied=%s Skipped=%s Failed=%s",
        results["Copied"],
        results["Skipped"],
        results["Failed"],
    )



if __name__ == "__main__":
    main()