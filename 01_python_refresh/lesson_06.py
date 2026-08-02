from pathlib import Path


# These are module-level constants.
# We define them once near the top because several parts of the program
# may eventually need to convert file sizes.
BYTES_PER_KB = 1024
BYTES_PER_MB = 1024 * BYTES_PER_KB
BYTES_PER_GB = 1024 * BYTES_PER_MB


def get_directory() -> Path | None:
    """
    Ask the user for a directory path and validate it.

    Keeps prompting until:
    - The user enters a valid folder.
    - The user enters 'q' to quit.

    Returns:
        A valid Path object, or None if the user quits.
    """
    print("Current working directory:", Path.cwd())
    print("Home directory:", Path.home())

    while True:
        user_input = (
            input("\nEnter a folder path (or 'q' to quit): ")
            .strip()
            .strip('"')
        )

        if user_input.lower() == "q":
            return None

        # expanduser() allows shortcuts such as:
        # ~
        # ~/Downloads
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
    Ask whether the scan should include nested subfolders.

    Returns:
        False for the current folder only.
        True for a recursive scan.
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

        if choice == "2":
            return True

        print("Please enter 1 or 2.")


def format_size(size_bytes: int) -> str:
    """
    Convert a raw byte count into a human-readable file size.

    The playful size labels are kept because they do not interfere
    with the actual file-size calculations.
    """
    # First, decide which playful category the file belongs to.
    if size_bytes < BYTES_PER_KB:
        label = "itty bitty"
    elif size_bytes < BYTES_PER_MB:
        label = "mousey"
    elif size_bytes < 3 * BYTES_PER_MB:
        label = "medium"
    elif size_bytes < 50 * BYTES_PER_MB:
        label = "biggun"
    else:
        label = "hella big"

    # Next, choose the most readable unit.
    # A 5 GB file should display as 5.0 GB instead of 5120.0 MB.
    if size_bytes < BYTES_PER_KB:
        readable = f"{size_bytes} B"
    elif size_bytes < BYTES_PER_MB:
        readable = f"{size_bytes / BYTES_PER_KB:.1f} KB"
    elif size_bytes < BYTES_PER_GB:
        readable = f"{size_bytes / BYTES_PER_MB:.1f} MB"
    else:
        readable = f"{size_bytes / BYTES_PER_GB:.1f} GB"

    return f"{readable} ({label})"


def inspect_directory(
    folder: Path,
    recursive: bool = False,
) -> dict[str, object]:
    """
    Inspect a directory and collect information about its contents.

    Counts:
    - Files
    - Folders
    - File extensions
    - Total items

    Also records:
    - The largest file
    - The largest file's size
    """
    file_count = 0
    folder_count = 0
    file_types: dict[str, int] = {}

    # None means that no file has been found yet.
    largest_file: Path | None = None

    # Starting at -1 ensures that a zero-byte file can still become
    # the largest file when it is the first file found.
    largest_size = -1

    try:
        absolute_path = folder.resolve()

        # rglob("*") scans every nested level.
        # iterdir() scans only the immediate folder.
        if recursive:
            items = folder.rglob("*")
        else:
            items = folder.iterdir()

        for item in items:
            if item.is_file():
                file_count += 1

                # Some files, such as LICENSE, have no extension.
                suffix = (
                    item.suffix.lower()
                    if item.suffix
                    else "(no extension)"
                )

                # Get the existing count for this suffix.
                # If it has not appeared before, begin at zero.
                file_types[suffix] = file_types.get(suffix, 0) + 1

                # stat().st_size gives the file size in bytes.
                size = item.stat().st_size

                # Replace the current largest file only when this
                # file is larger than the best one found so far.
                if size > largest_size:
                    largest_size = size
                    largest_file = item

            elif item.is_dir():
                folder_count += 1

    except PermissionError:
        return {
            "success": False,
            "error": (
                f"Access denied to '{folder}'.\n"
                "Your user account does not have permission "
                "to access this folder."
            ),
        }

    except OSError as error:
        return {
            "success": False,
            "error": (
                f"Something went wrong while accessing "
                f"'{folder}': {error}"
            ),
        }

    total_items = file_count + folder_count

    # folder.name can be empty for a drive root such as C:\.
    # In that case, display the complete path instead.
    display_name = folder.name or str(folder)

    return {
        "success": True,
        "name": display_name,
        "absolute_path": absolute_path,
        "recursive": recursive,
        "files": file_count,
        "folders": folder_count,
        "total_items": total_items,
        "file_types": dict(sorted(file_types.items())),
        "largest_file": largest_file,
        "largest_size": largest_size,
    }


def print_report(info: dict[str, object]) -> None:
    """
    Display the completed directory inspection report.
    """
    separator = "=" * 55

    if info["recursive"]:
        mode_label = "Recursive scan with subfolders"
    else:
        mode_label = "Current folder only"

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

    file_types = info["file_types"]

    # This program currently uses dict[str, object], so Python's type
    # checker may not know this value is a dictionary.
    # Runtime behavior is still correct.
    for suffix, count in file_types.items():
        print(f"  {suffix:<16} {count}")

    print()

    largest_file = info["largest_file"]
    largest_size = info["largest_size"]

    if largest_file is not None:
        print("Largest file:")
        print(f"  Path: {largest_file}")
        print(f"  Size: {format_size(largest_size)}")
    else:
        print("Largest file:  No files found")

    print(separator)


def main() -> None:
    """
    Coordinate the program's major steps.
    """
    folder = get_directory()

    if folder is None:
        print("\nProgram closed.")
        return

    recursive = get_scan_mode()

    info = inspect_directory(folder, recursive)

    # Every inspect_directory() result includes "success".
    # This allows main() to decide whether to display a report
    # or display an error.
    if not info["success"]:
        print(f"\nError: {info['error']}")
        return

    print_report(info)


if __name__ == "__main__":
    main()