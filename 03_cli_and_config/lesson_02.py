from pathlib import Path
import argparse


def count_files(
        source_folder: Path,
        recursive: bool,
) -> int:
    """
    Count files in the source folder.
    If recursive is True, include file subfolders.
    """

    if recursive:
        items = source_folder.rglob("*")
    else:
        items = source_folder.iterdir()

    file_count = 0

    for item in items:
        if item.is_file():
            file_count += 1

    return file_count

def validate_source_path(
        source_argument: str,
) -> Path | None:
    """
    Convert the source argument into a validated folder Path.
    """

    source_folder = Path(
        source_argument
    ).expanduser()

    if not source_folder.exists():
        print(
            f"Error: '{source_folder}' doesnt exist."
        )
        return None
    if not source_folder.is_dir():
        print(
            f"Error: '{source_folder}' is not a folder."
        )
        return None

    return source_folder

def parse_arguments() -> argparse.Namespace:
    """
    Define and parse command line arguments.
    """

    parser = argparse.ArgumentParser(
        description="Count files inside a source folder."
    )

    parser.add_argument(
        "--source",
        required=True,
        help="Folder containing the files to process.",
    )

    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Include files inside subfolders.",
    )

    return parser.parse_args()

def main() -> None:
    args = parse_arguments()

    source_folder = validate_source_path(
        args.source
    )

    if source_folder is None:
        return

    file_count = count_files(
        source_folder,
        args.recursive,
    )

    print(f"Files found: {file_count}")

if __name__ == "__main__":
    main()