from pathlib import Path


def get_directory() -> Path | None:
    """
    Ask the user for a directory path and validate it.
    Keeps prompting until a valid folder is given, or the user quits.
    """
    print("Current working directory:", Path.cwd())
    print("Home directory:", Path.home())

    while True:
        user_input = input("\nEnter a folder path (or 'q' to quit): ").strip().strip('"')

        if user_input.lower() == "q":
            return None

        folder = Path(user_input).expanduser()

        if not folder.exists():
            print(f"\nError: '{folder}' does not exist.")
            continue

        if not folder.is_dir():
            print(f"\nError: '{folder}' is not a directory.")
            continue

        return folder


def get_scan_mode() -> bool:
    """
    Ask the user whether to scan only the top-level folder
    or the folder plus all subfolders recursively.

    Returns:
        True for recursive scanning, False for top-level only.
    """
    while True:
        choice = input(
            "\nScan mode:\n"
            "  1) Current folder only\n"
            "  2) Current folder + all subfolders (recursive)\n"
            "Choose 1 or 2: "
        ).strip()

        if choice == "1":
            return False
        elif choice == "2":
            return True
        else:
            print("Please enter 1 or 2.")


def inspect_directory(folder: Path, recursive: bool = False) -> dict[str, object]:
    """
    Count files, folders, and all file types in a directory.
    """
    file_count = 0
    folder_count = 0
    file_types: dict[str, int] = {}

    try:
        absolute_path = folder.resolve()

        items = folder.rglob("*") if recursive else folder.iterdir()

        for item in items:
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
        "absolute_path": absolute_path,
        "recursive": recursive,
        "files": file_count,
        "folders": folder_count,
        "total_items": total_items,
        "file_types": dict(sorted(file_types.items())),
    }


def print_report(info: dict[str, object]) -> None:
    """
    Display the directory inspection results.
    """
    separator = "=" * 45
    mode_label = "Recursive (with subfolders)" if info["recursive"] else "Top-level only"

    print(f"\n{separator}")
    print("Directory Inspection Report")
    print(separator)
    print(f"Folder name:   {info['name']}")
    print(f"Absolute path: {info['absolute_path']}")
    print(f"Scan mode:     {mode_label}")
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

    recursive = get_scan_mode()

    info = inspect_directory(folder, recursive)

    if not info["success"]:
        print(f"\nError: {info['error']}")
        return

    print_report(info)


if __name__ == "__main__":
    main()