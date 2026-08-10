from datetime import datetime
from pathlib import Path
from typing import TypedDict



class FileInfo(TypedDict):
    name: str
    path: Path
    extension: str
    size_bytes: int
    modified: datetime


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


def get_file_info(
    file_path: Path,
) -> FileInfo:
    """
    Collect metadata about one file.
    Returns:
        Structured information describing the file.
    """
    stats = file_path.stat()

    modified_time = datetime.fromtimestamp(
        stats.st_mtime
    )

    return {
        "name": file_path.name,
        "path": file_path,
        "extension": (
            file_path.suffix.lower()
            if file_path.suffix
            else "(no extension)"
        ),
        "size_bytes": stats.st_size,
        "modified": modified_time,
    }

def collect_file_info(
    source_folder: Path,
) -> list[FileInfo]:
    """
    Collect metadata for files directly inside a folder.
    
    Returns:
        A list containing one FileInfo per file.
    """
    files: list[FileInfo] = []

    for item in source_folder.iterdir():
        if not item.is_file():
            continue

        info = get_file_info(item)
        files.append(info)

    return files

def print_file_info(
    files: list[FileInfo],
) -> None:
    """
    Display collected file metadata.
    """
    separator = "=" * 70

    print(f"\n{separator}")
    print("File Metadata Report")
    print(separator)

    if not files:
        print("No files found.")
        print(separator)
        return
    for info in files:
        modified = info["modified"].strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        print(f"Name:        {info['name']}")
        print(f"Extension:   {info['extension']}")
        print(f"Size:        {info['size_bytes']} bytes")
        print(f"Modified:    {modified}")
        print("-" * 70)

    print(f"Total files: {len(files)}")
    print(separator)

def main() -> None:
    source_folder = get_source_folder()

    if source_folder is None:
        return

    files = collect_file_info(source_folder)

    print_file_info(files)

if __name__ == "__main__":
    main()
