from collections import Counter
from pathlib import Path


def get_source_folder() -> Path | None:
    while True:
        user_input = (
            input("\nEnter source folder (or 'q' to quit): ")
            .strip()
            .strip('"')
        )

        if user_input.lower() == "  ":
            return None
        if not user_input:
            print("no path entered.")
            continue

        source_folder = Path(user_input).expanduser()

        if not source_folder.exists():
            print(f"Error: '{source_folder}' does not exist.")
            continue

        if not source_folder.is_dir():
            print(f"Error: '{source_folder}' is not a folder.")
            continue

        return source_folder

def get_name_prefix() -> str | None:
    """
    ask the usre for the prefix used when renaming files.
    Returns:
        a non-empty prefix, or None if the user quits.
    """
    while True:
        prefix = input(
            "\nEnter a filename prefix (or 'q' to quit): "
        ).strip()

        if prefix.lower() == "q":
            return None
        
        if not prefix:
            print("Prefix cannot be empty.")
            continue

        return prefix

def rename_files(
    source_folder: Path,
    prefix: str,
) -> Counter[str]:
    """
    Rename files in a folder using a prefix and sequence number.
    Existing folders are skipped.
    
    Returns:
        a Counter containing renamed, skipped, and failed totals.
    """
    results: Counter[str] = Counter()

    files = sorted(
        item
        for item in source_folder.iterdir()
        if item.is_file()
    )

    for index, item in enumerate(files, start=1):
        new_name = (
            f"{prefix}_{index:03d}"
            f"{item.suffix.lower()}"
        )

        destination = source_folder / new_name

        if destination.exists():
            results["Skipped existing"] += 1
            continue

        try:
            item.rename(destination)
            results["Renamed"] += 1

        except PermissionError:
            results["Failed"] += 1
            print(
                f"Error: Permission denied while renaming '{item.name}'."
            )

        except OSError as error:
            results["Failed"] += 1
            print(
                f"Error: Could not rename '{item.name}': {error}"
            )
    results["Skipped folders"] = sum(
        1
        for item in source_folder.iterdir()
        if item.is_dir()
    )        

    return results


def print_summary(
    results: Counter[str],
) -> None:
    """
    Display the batch rename results.
    """
    separator = "=" * 45

    print(f"\n{separator}")
    print("Batch Rename Summary")
    print(separator)

    print(f"{'Renamed:':<20} {results['Renamed']}")
    print(
        f"{'Skipped existing:':<20} "
        f"{results['Skipped existing']}"
    )
    print(
        f"{'Skipped folders:':<20} "
        f"{results['Skipped folders']}"
    )
    print(F"{'Failed:':<20} {results['Failed']}")

    print(separator)


def main() -> None:
    source_folder = get_source_folder()

    if source_folder is None:
        return

    prefix = get_name_prefix()

    if prefix is None:
        return

    results = rename_files(
        source_folder,
        prefix,
    )

    
    print_summary(results)


if __name__ == "__main__":
    main()