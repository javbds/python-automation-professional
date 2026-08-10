from collections import Counter
from pathlib import Path
import logging
import shutil


def configure_logging(
    log_file: Path,
) -> None:
    """
    Configure persistent file-based logging for the program.
    """
    log_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format=(
            "%(asctime)s | "
            "%(levelname)s | "
            "%(message)s"
        ),
    )


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
            return None

        if not user_input:
            print("No source path entered.")
            continue

        source_folder = Path(user_input).expanduser()

        if not source_folder.exists():
            print(
                f"Error: '{source_folder}' does not exist."
            )
            continue

        if not source_folder.is_dir():
            print(
                f"Error: '{source_folder}' is not a folder."
            )
            continue

        return source_folder


def get_archive_folder() -> Path | None:
    """
    Ask the user for an archive destination folder.

    If the folder does not exist, offer to create it.

    Returns:
        A valid archive folder Path, or None if the user quits.
    """
    while True:
        user_input = (
            input("\nEnter archive folder (or 'q' to quit): ")
            .strip()
            .strip('"')
        )

        if user_input.lower() == "q":
            return None

        if not user_input:
            print("No archive path entered.")
            continue

        archive_folder = Path(user_input).expanduser()

        if archive_folder.exists():
            if archive_folder.is_dir():
                return archive_folder

            print(
                f"Error: '{archive_folder}' exists "
                "but is not a folder."
            )
            continue

        create_choice = input(
            f"'{archive_folder}' does not exist. "
            "Create it? (y/n): "
        ).strip().lower()

        if create_choice != "y":
            print("Archive folder was not created.")
            continue

        try:
            archive_folder.mkdir(
                parents=True,
                exist_ok=True,
            )

            print(
                f"Created archive folder: "
                f"{archive_folder}"
            )

            return archive_folder

        except PermissionError:
            print(
                "Error: Permission denied while creating "
                f"'{archive_folder}'."
            )

        except OSError as error:
            print(
                f"Error: Could not create "
                f"'{archive_folder}': {error}"
            )


def get_extension_filter() -> set[str]:
    """
    Ask the user which file extensions should be archived.

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


def find_matching_files(
    source_folder: Path,
    extensions: set[str],
) -> list[Path]:
    """
    Recursively find files matching the selected extensions.

    Returns:
        A sorted list of matching file paths.
    """
    matching_files: list[Path] = []

    for item in source_folder.rglob("*"):
        if not item.is_file():
            continue

        if item.suffix.lower() not in extensions:
            continue

        matching_files.append(item)

    return sorted(matching_files)


def archive_files(
    files: list[Path],
    source_folder: Path,
    archive_folder: Path,
) -> Counter[str]:
    """
    Copy approved files into the archive while preserving
    their original directory structure.

    Existing archive files are skipped.

    Returns:
        A Counter containing copied, skipped, and failed totals.
    """
    results: Counter[str] = Counter()

    for file in files:
        relative_path = file.relative_to(
            source_folder
        )

        destination = (
            archive_folder / relative_path
        )

        if destination.exists():
            results["Skipped"] += 1

            logging.info(
                "Skipped existing file: %s",
                destination,
            )

            continue

        try:
            destination.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            shutil.copy2(
                file,
                destination,
            )

            results["Copied"] += 1

            logging.info(
                "Copied: %s -> %s",
                file,
                destination,
            )

        except PermissionError:
            results["Failed"] += 1

            logging.error(
                "Permission denied while copying: %s",
                file,
            )

        except OSError:
            results["Failed"] += 1

            logging.exception(
                "Failed to archive file: %s",
                file,
            )

    return results


def print_summary(
    results: Counter[str],
) -> None:
    """
    Display the archive operation results.
    """
    separator = "=" * 45

    print(f"\n{separator}")
    print("Archive Summary")
    print(separator)

    print(
        f"{'Files copied:':<20} "
        f"{results['Copied']}"
    )

    print(
        f"{'Files skipped:':<20} "
        f"{results['Skipped']}"
    )

    print(
        f"{'Files failed:':<20} "
        f"{results['Failed']}"
    )

    print(
        f"{'Total processed:':<20} "
        f"{sum(results.values())}"
    )

    print(separator)


def main() -> None:
    """
    Coordinate the safe file-archive workflow.
    """
    log_file = Path(
        "02_file_operations/logs/lesson_10.log"
    )

    configure_logging(log_file)

    logging.info("Archive program started.")

    source_folder = get_source_folder()

    if source_folder is None:
        logging.warning(
            "Archive operation cancelled before "
            "source selection."
        )
        return

    archive_folder = get_archive_folder()

    if archive_folder is None:
        logging.warning(
            "Archive operation cancelled before "
            "archive destination selection."
        )
        return

    extensions = get_extension_filter()

    files = find_matching_files(
        source_folder,
        extensions,
    )

    if not files:
        print("No matching files found.")

        logging.warning(
            "No matching files found in '%s'.",
            source_folder,
        )

        return

    logging.info(
        "Found %d matching files.",
        len(files),
    )

    results = archive_files(
        files,
        source_folder,
        archive_folder,
    )

    print_summary(results)

    logging.info(
        "Archive operation completed. "
        "Copied=%d Skipped=%d Failed=%d",
        results["Copied"],
        results["Skipped"],
        results["Failed"],
    )


if __name__ == "__main__":
    main()