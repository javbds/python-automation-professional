import shutil
from pathlib import Path

TEST_FOLDER = Path(
    "04_filesystem_automation/file_ops_test"
)

def rename_file(
    source: Path,
    destination: Path,
) -> bool:
    if not source.exists():
        print(f" Error: '{source}' doesnt exist.")
        return False

    if not source.is_file():
        print(f"Error '{source}' is not a file.")
        return False

    if destination.exists():
        print(f"Error: '{destination}' already exists.")
        return False

    source.rename(destination)

    return True

def ensure_directory(
    directory: Path
) -> bool:

    if directory.exists():
        if not directory.is_dir():
            print(f"Error: '{directory}' exits but is not a directory.")
            return False

        return True

    directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    return True

def copy_file(
    source: Path,
    destination: Path,
) -> bool:

    if not source.exists():
        print(
            f"Error: '{source}' does not exist."
        )
        return False

    if not source.is_file():
        print(
            f"Error: '{source}' is not a file."
        )
        return False

    if destination.exists():
        print(
            f"Error: '{destination}' already exists."
        )
        return False

    try:
        shutil.copy2(
            source,
            destination,
        )

    except OSError as error:
        print(
            f"Error: could not copy '{source}': {error}"
        )
        return False

    return True

def move_file(
    source: Path,
    destination: Path,
) -> bool:

    if not source.exists():
        print(
            f"Error: '{source}' does not exist."
        )
        return False

    if not source.is_file():
        print(
            f"Error: '{source}' is not a file."
        )
        return False

    if destination.exists():
        print(
            f"Error: '{destination}' already exists."
        )
        return False

    try:
        shutil.move(
            source,
            destination,
        )

    except OSError as error:
        print(
            f"Error: could not move '{source}': {error}"
        )
        return False

    return True

def verify_move(
    source: Path,
    destination: Path,
) -> bool:

    if source.exists():
        print(
            f"Error: source '{source}' still exists."
        )
        return False

    if not destination.exists():
        print(
            f"Error: destination '{destination}' "
            "does not exist."
        )
        return False

    return True

def main() -> None:
    source = (
        TEST_FOLDER 
        / "archive"
        / "old"
        / "photo.jpg"
    )

    destination = (
        TEST_FOLDER
        / "photo.jpg"
    )

    success = move_file(
        source,
        destination,
    )

    if not success:
        return

    verified = verify_move(
        source,
        destination,
    )

    if not verified:
        return

    print("Move completed and verified.")

    
if __name__ == "__main__":
    main()