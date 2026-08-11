from pathlib import Path
import sys


def validate_source_path(
    source_argument: str,
) -> Path | None:
    """
    Convert a raw source argument into a validated folder Path.
    Returns:
        A valid folder Path, or None if validation fails.
    """

    source_folder = Path(
        source_argument
    ).expanduser()

    if not source_folder.exists():
        print(
            f"Error: '{source_folder}' does not exist."
        )
        return None

    if not source_folder.is_dir():
        print(
            f"Error: '{source_folder}' is not a folder."
        )
        return None

    return source_folder

def count_files(
    source_folder: Path,
) -> int:
    """
    Count files directly inside the source folder.

    Returns:
        The number of files found.
    """
    file_count = 0

    for item in source_folder.iterdir():
        if item.is_file():
            file_count += 1

    return file_count

def get_source_argument() -> str | None:
    """
    Retrieve the first user-supplied command-line argument.

    Returns:
        The argument as a string, or None if it is missing.
    """
    if len(sys.argv) < 2:
        return None

    return sys.argv[1]


def main() -> None:
    source_argument = get_source_argument()

    if source_argument is None:
        print("Error: no source argument provided.")
        return

    source_folder = validate_source_path(
        source_argument
    )

    if source_folder is None:
        return

    file_count = count_files(
        source_folder
    )
    print(
        f"Files found: {file_count}")


if __name__ == "__main__":
    main()