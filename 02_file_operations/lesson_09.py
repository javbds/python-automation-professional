from pathlib import Path
import logging


def configure_logging(
    log_file: Path,
) -> None:
    """
    Configure file-based logging for the program.
    """
    log_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format=(
            "%(asctime)s | "
            "%(levelname)s | "
            "%(message)s"
        ),
    )


def run_demo_operations() -> None:
    """
    Generate sample log messages for testing.
    """
    logging.info("Program started.")
    logging.info("File operation completed.")
    logging.warning("Example warning generated.")
    logging.error("Example error generated.")

def inspect_folder(
    folder: Path,
) -> None:
    """
    Inspect a folder and log the results.
    """
    logging.info(
        "Starting folder inspection: %s",
        folder,
    )

    try:
        for item in folder.iterdir():
            if item.is_file():
                logging.info(
                    "Found file: %s",
                    item.name,
                )

            elif item.is_dir():
                logging.info(
                    "Found folder: %s",
                    item.name,
                )

        logging.info(
            "Folder inspection completed successfully."
        )

    except PermissionError:
        logging.error(
            "Permission denied while inspecting: %s",
            folder,
        )

    except OSError as error:
        logging.exception(
            "Could not inspect '%s'.",
            folder,
        )

def get_source_folder() -> Path | None:
    while True:
        user_input = (
            input("\nEnter source folder (or 'q' to quit): ")
            .strip()
            .strip('"')
        )

        if user_input.lower() == "q":
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
    
def main() -> None:
    log_file = Path(
        "02_file_operations/logs/lesson_09.log"
    )

    configure_logging(log_file)

    logging.info("Program started.")

    source_folder = get_source_folder()

    if source_folder is None:
        logging.warning(
            "Program cancelled by user."
        )
        return

    inspect_folder(source_folder)

    logging.info("Program finished.")

    print(f"Inspection complete. Check: {log_file}")


if __name__ == "__main__":
    main()