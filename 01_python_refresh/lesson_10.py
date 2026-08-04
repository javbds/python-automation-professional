from collections import Counter
from pathlib import Path
from typing import TypedDict


class DirectoryInfo(TypedDict):
    """
    Describe the exact structure returned by inspect_directory().
    """

    success: bool
    error: str | None
    name: str
    absolute_path: Path
    recursive: bool
    files: int
    folders: int
    total_items: int
    file_types: Counter[str]
    largest_file: Path | None
    largest_size: int
    skipped_items: list[str]
    skipped_count: int


# --------------------------------------------------------------------------
# Module-level constants
# --------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

BYTES_PER_KB = 1024
BYTES_PER_MB = 1024 * BYTES_PER_KB
BYTES_PER_GB = 1024 * BYTES_PER_MB

REPORT_SEPARATOR = "=" * 55

FORMAT_SIZE_TEST_CASES = [
    (0, "0 B (itty bitty)"),
    (512, "512 B (itty bitty)"),
    (1023, "1023 B (itty bitty)"),
    (1024, "1.0 KB (mousey)"),
    (1536, "1.5 KB (mousey)"),
    (1048575, "1024.0 KB (mousey)"),
    (1048576, "1.0 MB (medium)"),
    (3145727, "3.0 MB (medium)"),
    (3145728, "3.0 MB (biggun)"),
    (52428800, "50.0 MB (hella big)"),
    (1073741824, "1.0 GB (hella big)"),
    (5368709120, "5.0 GB (hella big)"),
]


def get_directory() -> Path | None:
    """
    Ask the user for a directory path and validate it.

    Returns:
        A valid Path object, or None if the user quits.
    """
    print("\nProject root:", PROJECT_ROOT)
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

        entered_path = Path(user_input).expanduser()

        if entered_path.is_absolute():
            folder = entered_path
        else:
            folder = PROJECT_ROOT / entered_path

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
    """
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

    if size_bytes < BYTES_PER_KB:
        readable = f"{size_bytes} B"
    elif size_bytes < BYTES_PER_MB:
        readable = f"{size_bytes / BYTES_PER_KB:.1f} KB"
    elif size_bytes < BYTES_PER_GB:
        readable = f"{size_bytes / BYTES_PER_MB:.1f} MB"
    else:
        readable = f"{size_bytes / BYTES_PER_GB:.1f} GB"

    return f"{readable} ({label})"


def create_error_result(
    folder: Path,
    recursive: bool,
    message: str,
) -> DirectoryInfo:
    """
    Create a complete DirectoryInfo result for a failed scan.

    Every DirectoryInfo result must contain the same keys.
    """
    return {
        "success": False,
        "error": message,
        "name": folder.name or str(folder),
        "absolute_path": folder,
        "recursive": recursive,
        "files": 0,
        "folders": 0,
        "total_items": 0,
        "file_types": Counter(),
        "largest_file": None,
        "largest_size": 0,
        "skipped_items": [],
        "skipped_count": 0,
    }


def inspect_directory(
    folder: Path,
    recursive: bool = False,
) -> DirectoryInfo:
    """
    Inspect a directory and collect information about its contents.
    """
    file_count = 0
    folder_count = 0
    file_types: Counter[str] = Counter()

    largest_file: Path | None = None
    largest_size = -1

    skipped_items: list[str] = []

    try:
        absolute_path = folder.resolve()

        if recursive:
            items = folder.rglob("*")
        else:
            items = folder.iterdir()

        for item in items:
            try:
                if item.is_file():
                    size = item.stat().st_size
                    file_count += 1

                    suffix = (
                        item.suffix.lower()
                        if item.suffix
                        else "(no extension)"
                    )

                    file_types[suffix] += 1

                    if size > largest_size:
                        largest_size = size
                        largest_file = item

                elif item.is_dir():
                    folder_count += 1

            except PermissionError:
                skipped_items.append(
                    f"{item}: Permission denied"
                )

            except FileNotFoundError:
                skipped_items.append(
                    f"{item}: Item disappeared during the scan"
                )

            except OSError as error:
                skipped_items.append(
                    f"{item}: {error}"
                )

    except PermissionError:
        return create_error_result(
            folder=folder,
            recursive=recursive,
            message=f"Permission denied while accessing '{folder}'.",
        )

    except FileNotFoundError:
        return create_error_result(
            folder=folder,
            recursive=recursive,
            message=f"'{folder}' disappeared during the scan.",
        )

    except OSError as error:
        return create_error_result(
            folder=folder,
            recursive=recursive,
            message=(
                f"Something went wrong while accessing "
                f"'{folder}': {error}"
            ),
        )

    total_items = file_count + folder_count
    display_name = folder.name or str(folder)

    return {
        "success": True,
        "error": None,
        "name": display_name,
        "absolute_path": absolute_path,
        "recursive": recursive,
        "files": file_count,
        "folders": folder_count,
        "total_items": total_items,
        "file_types": Counter(
            dict(sorted(file_types.items()))
        ),
        "largest_file": largest_file,
        "largest_size": largest_size,
        "skipped_items": skipped_items,
        "skipped_count": len(skipped_items),
    }


def run_format_size_tests() -> None:
    """
    Run all format_size() test cases and print a summary.
    """
    passed = 0
    failed = 0

    print("\nRunning format_size() tests...")
    print(REPORT_SEPARATOR)

    for size_bytes, expected in FORMAT_SIZE_TEST_CASES:
        actual = format_size(size_bytes)

        if actual == expected:
            passed += 1
            print(f"PASSED: {size_bytes:>12} bytes -> {actual}")
        else:
            failed += 1
            print(f"FAILED: {size_bytes:>12} bytes")
            print(f"  Expected: {expected}")
            print(f"  Actual:   {actual}")

    print(REPORT_SEPARATOR)
    print(f"Passed:      {passed}")
    print(f"Failed:      {failed}")
    print(f"Total tests: {len(FORMAT_SIZE_TEST_CASES)}")

    if failed == 0:
        print("All tests passed for format_size().")
    else:
        print("Some tests failed for format_size().")


def print_heading(title: str) -> None:
    """
    Print a titled section framed by separator lines.
    """
    print(f"\n{REPORT_SEPARATOR}")
    print(title)
    print(REPORT_SEPARATOR)


def print_key_value(
    label: str,
    value: object,
) -> None:
    """
    Print an aligned label and value.
    """
    print(f"{label:<14} {value}")


def print_file_type_counts(
    file_types: Counter[str],
) -> None:
    """
    Print one line for each file extension and count.
    """
    for suffix, count in file_types.items():
        print(f"  {suffix:<16} {count}")


def display_file_types(
    file_types: Counter[str],
) -> None:
    """
    Display the file-type summary section.
    """
    print()
    print("File types found:")

    if file_types:
        print_file_type_counts(file_types)
    else:
        print("  No files found.")


def print_report(info: DirectoryInfo) -> None:
    """
    Display the completed directory inspection report.
    """
    if info["recursive"]:
        mode_label = "Recursive scan with subfolders"
    else:
        mode_label = "Current folder only"

    print_heading("Directory Inspection Report")

    print_key_value("Folder name:", info["name"])
    print_key_value("Absolute path:", info["absolute_path"])
    print_key_value("Scan mode:", mode_label)

    print()
    print_key_value("Files:", info["files"])
    print_key_value("Folders:", info["folders"])
    print_key_value("Total items:", info["total_items"])
    print_key_value("Skipped items:", info["skipped_count"])

    display_file_types(info["file_types"])

    print()

    largest_file = info["largest_file"]
    largest_size = info["largest_size"]

    if largest_file is not None:
        print("Largest file:")
        print(f"  Path: {largest_file}")
        print(f"  Size: {format_size(largest_size)}")
    else:
        print("Largest file:  No files found")

    if info["skipped_items"]:
        print()
        print("Warnings:")

        for warning in info["skipped_items"]:
            print(f"  - {warning}")

    print(REPORT_SEPARATOR)


def get_program_mode() -> str:
    """
    Ask whether to inspect a directory or run tests.

    Returns:
        "normal" for directory inspection.
        "test" for format-size testing.
    """
    while True:
        choice = input(
            "\nProgram mode:\n"
            "  1) Normal operation\n"
            "  2) Run format_size() tests\n"
            "Choose 1 or 2: "
        ).strip()

        if choice == "1":
            return "normal"

        if choice == "2":
            return "test"

        print("Please enter 1 or 2.")


def main() -> None:
    """
    Coordinate the program's major workflows.
    """
    mode = get_program_mode()

    if mode == "test":
        run_format_size_tests()
        return

    folder = get_directory()

    if folder is None:
        print("\nProgram closed.")
        return

    recursive = get_scan_mode()
    info = inspect_directory(folder, recursive)

    if not info["success"]:
        print(f"\nError: {info['error']}")
        return

    print_report(info)


if __name__ == "__main__":
    main()