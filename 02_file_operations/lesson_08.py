from collections import Counter
from pathlib import Path
import shutil


def get_source_folder() -> Path | None:
    while True:
        user_input = (
            input("\nEnter source folder (or 'q' to quit): ")
            .strip()
            .strip('"')
        )

        if user_input.lower() == "q":
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


def get_backup_folder() -> Path | None:
    while True:
        user_input = (
            input("\nEnter backup folder (or 'q' to quit): ")
            .strip()
            .strip('"')
        )

        if user_input.lower() == "q":
            return None

        if not user_input:
            print("No backup path entered.")
            continue

        backup_folder = Path(user_input).expanduser()

        if backup_folder.exists():
            if backup_folder.is_dir():
                return backup_folder

            print(
                f"Error: '{backup_folder}' exists "
                "but is not a folder."
            )
            continue

        create_choice = input(
            f"'{backup_folder}' does not exist. "
            "Create it? (y/n): "
        ).strip().lower()

        if create_choice != "y":
            print("Backup folder was not created.")
            continue

        try:
            backup_folder.mkdir(
                parents=True,
                exist_ok=True,
            )

            print(
                f"Created backup folder: "
                f"{backup_folder}"
            )

            return backup_folder

        except PermissionError:
            print(
                "Error: Permission denied while creating "
                f"'{backup_folder}'."
            )

        except OSError as error:
            print(
                f"Error: Could not create "
                f"'{backup_folder}': {error}"
            )


def create_backup(
    source_folder: Path,
    backup_folder: Path,
) -> Counter[str]:
    """
    Copy files recursively into a backup folder while preserving
    the source directory structure.

    Returns:
        A Counter containing copied and failed totals.
    """
    results: Counter[str] = Counter()

    for item in source_folder.rglob("*"):
        if not item.is_file():
            continue

        relative_path = item.relative_to(source_folder)

        destination_file = (
            backup_folder / relative_path
        )

        try:
            destination_file.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            shutil.copy2(
                item,
                destination_file,
            )

            results["Copied"] += 1

        except PermissionError:
            results["Failed"] += 1

            print(
                f"Error: Permission denied while backing up "
                f"'{item}'."
            )

        except OSError as error:
            results["Failed"] += 1

            print(
                f"Error: Could not back up "
                f"'{item}': {error}"
            )

    return results


def print_summary(
    results: Counter[str],
) -> None:
    """
    Display the backup operation results.
    """
    separator = "=" * 45

    print(f"\n{separator}")
    print("Backup Summary")
    print(separator)

    print(f"{'Copied:':<20} {results['Copied']}")
    print(f"{'Failed:':<20} {results['Failed']}")

    print(separator)



def main() -> None:
    """
    Coordinate the backup workflow.
    """
    source_folder = get_source_folder()

    if source_folder is None:
        return

    backup_folder = get_backup_folder()

    if backup_folder is None:
        return

    results = create_backup(
        source_folder,
        backup_folder,
    )

    print_summary(results)
    
if __name__ == "__main__":
    main()