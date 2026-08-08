from pathlib import Path


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


def get_extension_filter() -> set[str]:
    while True:
        user_input = input(
            "\nEnter extensions separated by commas "
            "(example: .txt, .pdf, jpg): "
        ).strip()

        if not user_input:
            print("Please enter at least one extension.")
            continue

        extensions: set[str] = set()

        for extension in user_input.split(","):
            extension = extension.strip().lower()

            if not extension:
                continue

            if not extension.startswith("."):
                extension = "." + extension

            extensions.add(extension)

        if not extensions:
            print("No valid extensions were entered.")
            continue

        return extensions


def find_files_recursive(
    source_folder: Path,
    extensions: set[str],
) -> list[Path]:
    """
    Find matching files inside a folder and all subfolders.

    Returns:
        a sorted list of matching file paths.
    """

    matching_files: list[Path] =[]

    for item in source_folder.rglob("*"):
        if not item.is_file():
            continue

        if item.suffix.lower() not in extensions:
            continue
        matching_files.append(item)

    return sorted(matching_files)


def print_results(
    files: list[Path],
) -> None:
    """
    Display recursive search results.
    """

    print("\nMatching files:")

    if not files:
        print(" No matching files found.")
        return

    for file in files:
        print(f"  - {file}")

    print(f"\nTotal matches: {len(files)}")


def main() -> None:
    source_folder = get_source_folder()

    if source_folder is None:
        return

    extensions = get_extension_filter()

    files = find_files_recursive(
        source_folder,
        extensions,
    )

    print_results(files)

if __name__ == "__main__":
    main()