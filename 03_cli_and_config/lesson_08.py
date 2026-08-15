import argparse
import json
import os

from pathlib import Path
from typing import TypedDict


class AppConfig(TypedDict):
    source_folder: Path
    recursive: bool
    max_files: int
    extensions: list[str]


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Count matching files using configurable settings."
    )

    parser.add_argument(
        "--source",
        help="Override the source folder.",
    )

    parser.add_argument(
        "--recursive",
        action="store_true",
        default=None,
        help="Enable recursive scanning.",
    )

    parser.add_argument(
        "--max-files",
        type=int,
        help="Override the maximum number of files.",
    )

    return parser.parse_args()

def load_config(
    config_path: Path,
) -> dict | None:
    try:
        with config_path.open(
            "r",
            encoding="utf-8",
        ) as file:
            return json.load(file)

    except FileNotFoundError:
        print(
            f"Error: Config file '{config_path}' was not found."
        )
        return None

    except json.JSONDecodeError as error:
        print(
            f"Error: Invalid JSON in '{config_path}'."
        )
        print(
            f"Line {error.lineno}, column {error.colno}: {error.msg}"
        )
        return None

    except OSError as error:
        print(
            f"Error: could not read '{config_path}': {error}"
        )
        return None

def resolve_source_folder(
    cli_source: str | None,
    config: dict,
) -> Path | None:

    if cli_source is not None:
        source_value = cli_source
    else:
        source_value = config.get(
            "source_folder"
        )

    if source_value is None:
        print(
            "Error: source folder was not provided "
            "by CLI or JSON."
        )
        return None

    if not isinstance(source_value, str):
        print(
            "Error: source folder must be a string."
        )
        return None

    source_folder = Path(
        source_value
    ).expanduser()

    if not source_folder.exists():
        print(
            f"Error: '{source_folder}' does not exist."
        )
        return None

    if not source_folder.is_dir():
        print(
            f"Error: '{source_folder}' is not a folder."
        )
        return None

    return source_folder

def resolve_recursive(
    cli_recursive: bool | None,
    config: dict,
) -> bool | None:

    if cli_recursive is not None:
        return cli_recursive

    json_value = config.get(
        "recursive"
    )

    if json_value is None:
        print(
            "Error: 'recursive' was not provided "
            "by CLI or JSON."
        )
        return None

    if not isinstance(json_value, bool):
        print(
            "Error: JSON 'recursive' "
            "must be a Boolean."
        )
        return None

    return json_value

def resolve_max_files(
    cli_value: int | None,
    config: dict,
) -> int | None:

    if cli_value is not None:
        if cli_value <= 0:
            print(
                "Error: --max-files must be "
                "greater than zero."
            )
            return None

        return cli_value

    environment_value = os.environ.get(
        "MAX_FILES"
    )

    if environment_value is not None:
        try:
            max_files = int(
                environment_value
            )

        except ValueError:
            print(
                "Error: MAX_FILES environment "
                "variable must be a whole number."
            )
            return None

        if max_files <= 0:
            print(
                "Error: MAX_FILES must be "
                "greater than zero."
            )
            return None

        return max_files

    json_value = config.get(
        "max_files"
    )

    if not isinstance(json_value, int):
        print(
            "Error: JSON 'max_files' "
            "must be an integer."
        )
        return None

    if json_value <= 0:
        print(
            "Error: JSON 'max_files' must "
            "be greater than zero."
        )
        return None

    return json_value

def resolve_extensions(
    config: dict,
) -> list[str] | None:

    extensions = config.get(
        "extensions"
    )

    if extensions is None:
        print(
            "Error: JSON 'extensions' is missing."
        )
        return None

    if not isinstance(extensions, list):
        print(
            "Error: JSON 'extensions' must be a list."
        )
        return None

    for extension in extensions:
        if not isinstance(extension, str):
            print(
                "Error: every extension must be a string."
            )
            return None

    return extensions

def create_app_config(
        source_folder: Path,
        recursive: bool,
        max_files: int,
        extensions: list[str],
) -> AppConfig:

    return {
        "source_folder": source_folder,
        "recursive": recursive,
        "max_files": max_files,
        "extensions": extensions,
    }


def count_matching_files(
    config: AppConfig,
) -> int:
    file_count = 0

    if config["recursive"]:
        iterator = config["source_folder"].rglob("*")
    else:
        iterator = config["source_folder"].iterdir()

    for item in iterator:
        if not item.is_file():
            continue

        if item.suffix.lower() not in config["extensions"]:
            continue

        file_count += 1

        if file_count >= config["max_files"]:
            break

    return file_count

def main() -> None:
    args = parse_arguments()

    config_path = Path(
        "03_cli_and_config/lesson_08_config.json"
    )

    config = load_config(
        config_path
    )

    if config is None:
        return

    source_folder = resolve_source_folder(
        args.source,
        config,
    )

    if source_folder is None:
        return

    recursive = resolve_recursive(
        args.recursive,
        config,
    )

    if recursive is None:
        return

    max_files = resolve_max_files(
        args.max_files,
        config
    )

    if max_files is None:
        return

    extensions = resolve_extensions(
        config
    )

    if extensions is None:
        return

    app_config = create_app_config(
            source_folder,
            recursive,
            max_files,
            extensions,
        )

    file_count = count_matching_files(
        app_config
    )

    print("\n--- Results ---")
    print(f"Source: {app_config['source_folder']}")
    print(f"Recursive: {app_config['recursive']}")
    print(f"Extensions: {app_config['extensions']}")
    print(f"Maximum files: {app_config['max_files']}")
    print(f"Matching files: {file_count}")
    

if __name__ == "__main__":
    main()