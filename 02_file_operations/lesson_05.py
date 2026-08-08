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


def get_extension_filter() -> set[str]:
    while True:
        user_input = input(
            "\nEnter extensions separated by commas "
            "(example: .txt, .pdf, jpg): "
        ).strip()

        if not user_input:
            print("Please enter at least one extension.")
            continue

        extensions: set[str] = set()

        for extension in user_input.split(","):
            extension = extension.strip().lower()

            if not extension:
                continue

            if not extension.startswith("."):
                extension = "." + extension

            extensions.add(extension)

        if not extensions:
            print("No valid extensions were entered.")
            continue

        return extensions


def find_matching_files(
    source_folder: Path,
    extensions: set[str],
) -> list[Path]:
    """
    Find files whose extensions match the requested filter.
    
    Returns:
        a sorted list of matching file paths.
    """
    matching_files: list[Path] = []

    for item in source_folder.iterdir():
        if not item.is_file():
            continue

        if item.suffix.lower() not in extensions:
            continue

        matching_files.append(item)

    return sorted(matching_files)

def preview_files(
    files: list[Path],
) -> None:
    """
    Display files that are candidates for deletion.
    """
    print("\nFiles selected for deletion:")

    if not files:
        print("  No matching files found.")
        return

    for file in files:
        print(f"  - {file.name}")

    print(f"\nTotal selected: {len(files)}")


def confirm_deletion() -> bool:
    """
    Ask the user to confirm the destructive operation.

    Returns:
        True only when the user explicitly enters 'y'.
    """
    choice = input(
        "\nDelete these files? (y/n): "
    ).strip().lower()

    return choice == "y"


def delete_files(
    files: list[Path],
) -> Counter[str]:
    """
    Delete approved files and record the results.

    Returns:
        A Counter containing deleted, missing, and failed totals.
    """
    results: Counter[str] = Counter()

    for file in files:
        if not file.exists():
            results["Missing"] += 1
            continue

        try:
            file.unlink()
            results["Deleted"] += 1

        except PermissionError:
            results["Failed"] += 1
            print(
                f"Error: Permission denied while deleting "
                f"'{file.name}'."
            )

        except OSError as error:
            results["Failed"] += 1
            print(
                f"Error: Could not delete "
                f"'{file.name}': {error}"
            )

    return results

def print_summary(
    results: Counter[str],
) -> None:
    """
    Display the deletion results.
    """
    separator = "=" * 45

    print(f"\n{separator}")
    print("File Deletion Summary")
    print(separator)

    print(f"{'Deleted:':<20} {results['Deleted']}")
    print(f"{'Missing:':<20} {results['Missing']}")
    print(f"{'Failed:':<20} {results['Failed']}")

    print(separator)


def main() -> None:
    """
    Coordinate the safe file-deletion workflow.
    """
    source_folder = get_source_folder()

    if source_folder is None:
        return

    extensions = get_extension_filter()

    matching_files = find_matching_files(
        source_folder,
        extensions,
    )

    preview_files(matching_files)

    if not matching_files:
        return

    if not confirm_deletion():
        print("Deletion cancelled. No files were changed.")
        return

    results = delete_files(matching_files)

    print_summary(results)


if __name__ == "__main__":
    main()