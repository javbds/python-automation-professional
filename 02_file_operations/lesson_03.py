from collections import Counter
from pathlib import Path
import shutil


def get_source_folder() -> Path | None:
    """
    Ask the user for an existing source folder.

    Returns:
        A valid source folder Path, or None if the user quits.
    """
    while True:
        user_input = (
            input("\nEnter source folder (or 'q' to quit): ")
            .strip()
            .strip('"')
        )

        if user_input.lower() == "q":
            print("Quitting.")
            return None

        if not user_input:
            print("No path entered.")
            continue

        source_folder = Path(user_input).expanduser()

        if not source_folder.exists():
            print(f"Error: '{source_folder}' does not exist.")
            continue

        if not source_folder.is_dir():
            print(f"Error: '{source_folder}' is not a folder.")
            continue

        return source_folder


def get_destination_folder() -> Path | None:
    """
    Ask the user for a destination folder.

    If it does not exist, offer to create it.

    Returns:
        A valid destination folder Path, or None if the user quits.
    """
    while True:
        user_input = (
            input("\nEnter destination folder (or 'q' to quit): ")
            .strip()
            .strip('"')
        )

        if user_input.lower() == "q":
            return None

        if not user_input:
            print("No destination path entered.")
            continue

        destination_folder = Path(user_input).expanduser()

        if destination_folder.exists():
            if destination_folder.is_dir():
                return destination_folder

            print(
                f"Error: '{destination_folder}' exists "
                "but is not a folder."
            )
            continue

        create_choice = input(
            f"'{destination_folder}' does not exist. "
            "Create it? (y/n): "
        ).strip().lower()

        if create_choice != "y":
            print("Destination folder was not created.")
            continue

        try:
            destination_folder.mkdir(
                parents=True,
                exist_ok=True,
            )

            print(
                f"Created destination folder: "
                f"{destination_folder}"
            )

            return destination_folder

        except PermissionError:
            print(
                "Error: Permission denied while creating "
                f"'{destination_folder}'."
            )

        except OSError as error:
            print(
                f"Error: Could not create "
                f"'{destination_folder}': {error}"
            )


def get_extension_filter() -> set[str]:
    """
    Ask which file extensions should be copied.

    Returns:
        A normalized set of lowercase extensions.
    """
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


def copy_matching_files(
    source_folder: Path,
    destination_folder: Path,
    extensions: set[str],
) -> Counter[str]:
    """
    Copy files whose extensions match the requested filter.

    Existing destination files are skipped rather than overwritten.

    Returns:
        A Counter containing operation results.
    """
    results: Counter[str] = Counter()

    for item in source_folder.iterdir():

        if not item.is_file():
            results["Skipped folders"] += 1
            continue

        suffix = item.suffix.lower()

        if suffix not in extensions:
            results["Skipped files"] += 1
            continue

        destination_file = destination_folder / item.name

        # Do not silently overwrite existing files.
        if destination_file.exists():
            results["Skipped existing"] += 1
            continue

        try:
            shutil.copy2(
                item,
                destination_file,
            )

            results["Copied"] += 1

        except PermissionError:
            results["Failed"] += 1
            print(
                f"Error: Permission denied while copying "
                f"'{item}'."
            )

        except OSError as error:
            results["Failed"] += 1
            print(
                f"Error: Could not copy '{item}': {error}"
            )

    return results


def print_summary(
    results: Counter[str],
) -> None:
    """
    Display the results of the filtered copy operation.
    """
    separator = "=" * 45

    print(f"\n{separator}")
    print("Filtered File Copy Summary")
    print(separator)

    print(f"{'Copied:':<20} {results['Copied']}")
    print(
        f"{'Skipped files:':<20} "
        f"{results['Skipped files']}"
    )
    print(
        f"{'Skipped folders:':<20} "
        f"{results['Skipped folders']}"
    )
    print(
        f"{'Skipped existing:':<20} "
        f"{results['Skipped existing']}"
    )
    print(f"{'Failed:':<20} {results['Failed']}")

    print(separator)


def main() -> None:
    """
    Coordinate the filtered file-copy workflow.
    """
    source_folder = get_source_folder()

    if source_folder is None:
        return

    destination_folder = get_destination_folder()

    if destination_folder is None:
        return

    extensions = get_extension_filter()

    results = copy_matching_files(
        source_folder,
        destination_folder,
        extensions,
    )

    print_summary(results)


if __name__ == "__main__":
    main()