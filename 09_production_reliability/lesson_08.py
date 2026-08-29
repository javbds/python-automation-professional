import logging
from pathlib import Path


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s: %(message)s"
    )


def ensure_directory(path):
    directory = Path(path)

    if directory.exists():
        logging.info("Directory already exists: %s", directory)
        return directory

    directory.mkdir()
    logging.info("Directory created: %s", directory)

    return directory

def main():
    setup_logging()

    ensure_directory("automation_output")


if __name__ == "__main__":
    main()