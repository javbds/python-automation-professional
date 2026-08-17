from collections import Counter
from pathlib import Path
import shutil


TEST_ROOT = Path(
    "04_filesystem_automation/batch_test"
)

def copy_files(
    files: list[Path],
    destination_folder: Path,
) -> Counter[str]:
    results: Counter[str] = Counter()

    try:
        destination_folder.mkdir(
            parents=True,
            exist_ok=True
        )

    except OSError as error:
        print(f"Error: could not prepare destination '{destination_folder}' : {error}")

        results["Failed"] += len(files)
        return results
    
    for source in files:
        destination = (
            destination_folder / source.name
        )

        if not source.exists():
            results["Failed"] += 1
            continue

        if not source.is_file():
            results["Skipped"] += 1

        if destination.exists():
            results["Skipped"] += 1
            continue

        try:
            shutil.copy2(
                source,
                destination,
            )

            results["Copied"] += 1

        except OSError:
            results["Failed"] += 1

    return results

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

    print("Files selected:")

    for file in files:
        print(f"- {file.name}")

    results = copy_files(
        files,
        destination_folder,
    )

    print_summary(results)

if __name__ == "__main__":
    main()