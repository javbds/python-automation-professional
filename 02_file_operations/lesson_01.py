from pathlib import Path
import shutil


def get_source_file() -> Path | None:
    """
    Ask the user for a source file and validate it.

    Returns:
        A valid file Path, or None if the user quits.
    """
    while True:
        user_input = (
            input("\nEnter a file path (or 'q' to quit): ")
            .strip()
            .strip('"')
        )

        if user_input.lower() == "q":
            print("Quitting.")
            return None

        if not user_input:
            print("No path entered.")
            continue

        source_file = Path(user_input).expanduser()

        if not source_file.exists():
            print(f"\nError: '{source_file}' does not exist.")
            continue

        if not source_file.is_file():
            print(f"\nError: '{source_file}' is not a file.")
            continue

        return source_file


def get_destination_folder() -> Path | None:
    """
    Ask the user for a destination folder.

    If the folder does not exist, offer to create it.

    Returns:
        A valid destination Path, or None if the user quits.
    """
    while True:
        user_input = (
            input("\nEnter a destination folder (or 'q' to quit): ")
            .strip()
            .strip('"')
        )

        if user_input.lower() == "q":
            return None

        if not user_input:
            print("No destination path entered.")
            continue

        destination = Path(user_input).expanduser()

        if destination.exists():
            if destination.is_dir():
                return destination

            print(
                f"Error: '{destination}' exists but is not a folder."
            )
            continue

        create_choice = input(
            f"'{destination}' doesn't exist. Create it? (y/n): "
        ).strip().lower()

        if create_choice != "y":
            print("Destination folder was not created.")
            continue

        try:
            destination.mkdir(parents=True, exist_ok=True)
            print(f"Created destination folder: {destination}")
            return destination

        except PermissionError:
            print(
                f"Error: Permission denied while creating "
                f"'{destination}'."
            )

        except OSError as error:
            print(
                f"Error: Couldn't create '{destination}': {error}"
            )


def copy_file(
    source: Path,
    destination: Path,
) -> bool:
    """
    copy source fie into destination folder.
    
    if a file with the same name exists, ask before overwriting
    
    Returns:
        True when the file is copied.
        False when the copy is canceleed or fails.
    """
    destination_file = destination / source.name

    if destination_file.exists():
        overwrite_choice = input(
            f"' {destination_file}' already exists." "Overwrite? (y/n): "
        ).strip().lower()

        if overwrite_choice != "y":
            print("copy cancelled. Existing file wasn't changed.")
            return False

    try:
        shutil.copy2(source, destination_file)
        print(f"Copied succesfully: {destination_file}")
        return True

    except PermissionError:
        print(
            "Error: Permission denied while copying" f"'{source}' to '{destination_file}'."
        )
        return False

    except OSError as error:
        print(f"Error: Could not copy the file: {error}")
        return False


def main() -> None:
    source_file = get_source_file()

    if source_file is None:
        return
    
    destination_folder = get_destination_folder()

    if destination_folder is None:
        return

    copied = copy_file(
        source_file,
        destination_folder,
    )

    if copied:
        print("File-copy operation completed.")
    else:
        print("File-copy operation did not complete.")


if __name__ == "__main__":
    main()