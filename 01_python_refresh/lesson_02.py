from pathlib import Path


def get_directory() -> Path | None:
    """
    Ask the user for a directory path and validate it.

    Returns:
        A valid Path object, or None if the path is invalid.
    """
    print("Current working directory:", Path.cwd())
    print("Home directory:", Path.home())

    folder = Path(input("\nEnter a folder path: ").strip())

    if not folder.exists():
        print(f"\nError: '{folder}' does not exist.")
        return None

    if not folder.is_dir():
        print(f"\nError: '{folder}' is not a directory.")
        return None

    return folder


def inspect_directory(folder: Path) -> dict[str, object]:
    """
    Count files, folders, and selected file types in a directory.
    """
    file_count = 0
    folder_count = 0
    python_count = 0
    text_count = 0
    pdf_count = 0

    for item in folder.iterdir():
        if item.is_file():
            file_count += 1

            suffix = item.suffix.lower()

            if suffix == ".py":
                python_count += 1
            elif suffix == ".txt":
                text_count += 1
            elif suffix == ".pdf":
                pdf_count += 1

        elif item.is_dir():
            folder_count += 1

    total_items = file_count + folder_count

    return {
        "name": folder.name,
        "absolute_path": folder.resolve(),
        "files": file_count,
        "folders": folder_count,
        "total_items": total_items,
        "python_files": python_count,
        "text_files": text_count,
        "pdf_files": pdf_count,
    }


def print_report(info: dict[str, object]) -> None:
    """
    Display the directory inspection results.
    """
    separator = "=" * 45

    print(f"\n{separator}")
    print("Directory Inspection Report")
    print(separator)
    print(f"Folder name:     {info['name']}")
    print(f"Absolute path:   {info['absolute_path']}")
    print()
    print(f"Files:           {info['files']}")
    print(f"Folders:         {info['folders']}")
    print(f"Total items:     {info['total_items']}")
    print()
    print(f"Python files:    {info['python_files']}")
    print(f"Text files:      {info['text_files']}")
    print(f"PDF files:       {info['pdf_files']}")
    print(separator)


def main() -> None:
    """
    Run the directory inspection program.
    """
    folder = get_directory()

    if folder is None:
        return

    info = inspect_directory(folder)
    print_report(info)


if __name__ == "__main__":
    main()