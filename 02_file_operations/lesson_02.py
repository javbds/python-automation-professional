from pathlib import Path
import shutil
from collections import Counter



def get_source_folder() -> Path | None:
    """
    Ask the user for a source folder and validate.
    Returns:
        a valid folder path, or None if the user quits
    """
    while True:
        user_input = (
            input("\nEnter source folder (or 'q' to quit): ")
            .strip()
            .strip('"')
        )

        if user_input.lower() == "q":
            print("Quitting.")
            return None

        if not user_input:
            print("No path entered.")
            continue

        source_folder = Path(user_input).expanduser()

        if not source_folder.exists():
            print(f"\nError: '{source_folder}' does not exist.")
            continue

        if not source_folder.is_dir():
            print(f"\nError: '{source_folder}' is not a folder.")
            continue

        return source_folder

def determine_destination(
    file_path: Path,
    destination_root: Path,
) -> Path:
    """
    Determine the category folder for a file based on suffix
    Returns:
        The destination cat Path. The folder is not created here.
    """
    suffix = file_path.suffix.lower()

    if suffix in {".jpg", ".jpeg", ".png", ".webp"}:
        category = "Images"

    elif suffix == ".pdf":
        category = "PDF"

    elif suffix in {".txt", ".md"}:
        category = "Text"

    elif suffix in {".csv", ".xlsx", ".xls"}:
        category = "Spreadsheets"

    elif suffix in {".doc", ".docx"}:
        category = "Documents"

    elif suffix in {".zip", ".rar", ".7z"}:
        category = "Archives"

    elif not suffix:
        category = "No_Extension"

    else:
        category = "Other"

    return destination_root / category
    


def move_file(
    source: Path,
    destination: Path,
) -> bool:
    """
    Move a source file into a destination folder safely.
    Returns:
        True if the move succeeds.
        False if it is cancelled or fails.
    """
    try:
        destination.mkdir(parents=True, exist_ok=True)

    except PermissionError:
        print(
            f"Error: Permission denied while creating '{destination}'."
        )
        return False

    except OSError as error:
        print(
            f"Error: could not create '{destination}': {error}"
        )
        return False

    destination_file = destination / source.name

    if destination_file.exists():
        overwrite_choice = input(
            f"'{destination_file}' already exists. " "overwrite? (y/n): "
        ).strip().lower()

        if overwrite_choice != "y":
            print("move cancelled. Existing file was not changed.")
            return False

        try:
            destination_file.unlink()

        except PermissionError:
            print(
                f"Error: Permission denied while replacing '{destination_file}'."
            )
            return False

        except OSError as error:
            print(
                f"Error: could not replace '{destination_file}': {error}"
            )
            return False

        
    try:
        shutil.move(source, destination_file)
        print(f"Moved: {source.name} -> {destination}")
        return True

    except PermissionError:
        print(
            f"Error: Permission denied while moving '{source}'."
        )
        return False

    except OSError as error:
        print(f"Error: could not move '{source}': {error}")
        return False


def organize_folder(
    source_folder: Path,
    destination_root: Path,
) -> Counter[str]:
    """
    Organize files from a source foldr into category folders.
    Only files directly inside the source folder are processed.
    subfolders are skipped.
    Returns
        a Counter containing successful catergory counts and failurs.
    """
    results: Counter[str] = Counter()

    for item in source_folder.iterdir():
        if not item.is_file():
            results["Skipped folders"] += 1
            continue

        destination = determine_destination(
            item,
            destination_root,
        )

        moved = move_file(
            item,
            destination,
        )

        if moved:
            results[destination.name] += 1
        else:
            results["Failed"] += 1

    return results 
def print_summary(
    results: Counter[str],
) -> None:
    """    
    Display the results of the folder organization operation
    """
    separator = "=" * 45

    print(f"\n{separator}")
    print("File Organization Summary")
    print(separator)

    if not results:
        print("No items were processed.")
        print(separator)
        return

    total_moved = 0

    for category, count in sorted(results.items()):
        print(f"{category:<20} {count}")

        if category not in {"Failed", "Skipped folders"}:
            total_moved += count 

    print(separator)
    print(f"{'Files moved:':<20} {total_moved}")
    print(f"{'Failed:':<20} {results['Failed']}")
    print(
        f"{'Folders skipped:':>20}"
        f"{results['Skipped folders']}"
        )
    print(separator)


def main() -> None:
    """
     Coordinate the folder organization workflow
     """
    source_folder = get_source_folder()

    if source_folder is None:
        return

    destination_root = source_folder / "organized_output"

    results = organize_folder(
        source_folder,
        destination_root,
    )

    print_summary(results)

if __name__ == "__main__":
    main()