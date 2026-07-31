from pathlib import Path


def get_directory() -> Path | None:
    """
    Ask the user for a directory path and validate it.

    Returns:
        A valid Path object, or None if the path is invalid.
    """
    print("Current working directory:", Path.cwd())
    print("Home directory:", Path.home())

    user_input = input("\nEnter a folder path: ").strip().strip('"')
    folder = Path(user_input).expanduser()

    if not folder.exists():
        print(f"\nError: '{folder}' does not exist.")
        return None

    if not folder.is_dir():
        print(f"\nError: '{folder}' is not a directory.")
        return None

    return folder


def inspect_directory(folder: Path) -> dict[str, object]:
    """
    Count files, folders, and all file types in a directory.
    """
    file_count = 0
    folder_count = 0
    file_types: dict[str, int] = {}

    try:
        absolute_path = folder.resolve()

        for item in folder.iterdir():
            if item.is_file():
                file_count += 1
                suffix = item.suffix.lower() if item.suffix else "(no extension)"
                file_types[suffix] = file_types.get(suffix, 0) + 1

            elif item.is_dir():
                folder_count += 1

    except PermissionError:
        return {
            "success": False,
            "error": ( 
                f"Access denied to '{folder}'.\n"
            "Your user account does not have permission to access this folder."
            ),
        }
    
    except OSError as error:
        return {
            "success": False,
            "error": f"Something went wrong while accessing '{folder}': {error}",
        }
    total_items = file_count + folder_count

    return {
        "success": True,
        "name": folder.name,
        "absolute_path": folder.resolve(),
        "files": file_count,
        "folders": folder_count,
        "total_items": total_items,
        "file_types": dict(sorted(file_types.items())),
    }


def print_report(info: dict[str, object]) -> None:
    """
    Display the directory inspection results alphabetically.
    """
    separator = "=" * 45

    print(f"\n{separator}")
    print("Directory Inspection Report")
    print(separator)
    print(f"Folder name:   {info['name']}")
    print(f"Absolute path: {info['absolute_path']}")
    print()
    print(f"Files:         {info['files']}")
    print(f"Folders:       {info['folders']}")
    print(f"Total items:   {info['total_items']}")
    print()
    print("File types found:")
    for suffix, count in info["file_types"].items():
        print(f"  {suffix:<16} {count}")
    print(separator)


def main() -> None:
    """
    Run the directory inspection program.
    """
    folder = get_directory()

    if folder is None:
        return

    info = inspect_directory(folder)

    if not info["success"]:
        print(f"\nError: {info['error']}")
        return
    print_report(info)


if __name__ == "__main__":
    main()