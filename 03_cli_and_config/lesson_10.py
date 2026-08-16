import argparse
import json
import sys
import os

from pathlib import Path
from typing import TypedDict



BYTES_PER_KB = 1024
BYTES_PER_MB = 1024 ** 2
BYTES_PER_GB = 1024 ** 3

EXIT_SUCCESS = 0
EXIT_INVALID_INPUT = 2
EXIT_OPERATION_ERROR = 1

class AppConfig(TypedDict):
    source_folder: Path
    recursive: bool
    max_files: int
    extensions: list[str]

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scan folder for matching files and report on them."
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
            f"Error: Config file '{config_path}' was not found.",
            file=sys.stderr
        )
        return None

    except json.JSONDecodeError as error:
        print(
            f"Error: Invalid JSON in '{config_path}'.",
            file=sys.stderr
        )
        print(
            f"Line {error.lineno}, column {error.colno}: {error.msg}",
            file=sys.stderr
        )
        return None

    except OSError as error:
        print(
            f"Error: could not read '{config_path}': {error}",
            file=sys.stderr
        )
        return None

def resolve_source_folder(
    cli_source: str | None,
    config: dict,
) -> Path | None:

    source_value = cli_source if cli_source is not None else config.get("source_folder")

    if source_value is None:
        print(
            "Error: source folder was not provided "
            "by CLI or JSON.",
            file=sys.stderr
        )
        return None

    if not isinstance(source_value, str):
        print(
            "Error: source folder must be a string.",
            file=sys.stderr
        )
        return None

    source_folder = Path(
        source_value
    ).expanduser()

    if not source_folder.exists():
        print(
            f"Error: '{source_folder}' does not exist.",
            file=sys.stderr
        )
        return None

    if not source_folder.is_dir():
        print(
            f"Error: '{source_folder}' is not a folder.",
            file=sys.stderr
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
            "by CLI or JSON.",
            file=sys.stderr
        )
        return None

    if not isinstance(json_value, bool):
        print(
            "Error: JSON 'recursive' "
            "must be a Boolean.",
            file=sys.stderr
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
                "greater than zero.",
                file=sys.stderr
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
                "variable must be a whole number.",
                file=sys.stderr,
            )
            return None

        if max_files <= 0:
            print(
                "Error: MAX_FILES must be "
                "greater than zero.",
                file=sys.stderr,
            )
            return None

        return max_files

    if "max_files" in config:
        json_value = config["max_files"]

        if not isinstance(json_value, int):
            print(
            "Error: JSON 'max_files' "
            "must be an integer.",
            file=sys.stderr,
            )
            return None

        if json_value <= 0:
            print(
            "Error: JSON 'max_files' must "
            "be greater than zero.",
            file=sys.stderr
            )
            return None

        return json_value
    return 100

def resolve_extensions(
    config: dict,
) -> list[str] | None:

    extensions = config.get(
        "extensions"
    )

    if extensions is None:
        print(
            "Error: JSON 'extensions' is missing.",
            file=sys.stderr
        )
        return None

    if not isinstance(extensions, list):
        print(
            "Error: JSON 'extensions' must be a list.",
            file=sys.stderr
        )
        return None
    normalized: list[str] = []

    for extension in extensions:
        if not isinstance(extension, str):
            print(
                "Error: every extension must be a string.",
                file=sys.stderr
            )
            return None
        normalized.append(extension.lower())

    return normalized

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
) -> tuple[int,int] | None:
    file_count = 0
    total_size = 0
    source = config["source_folder"]

    try:
        iterator = source.rglob("*") if config["recursive"] else source.iterdir()

        for item in iterator:
            if not item.is_file():
                continue

            if item.suffix.lower() not in config["extensions"]:
                continue

            try: 
                size = item.stat().st_size
            except OSError as error:
                print(f"Warning: could not read '{item}' : {error}",
                      file=sys.stderr)
                continue

            file_count += 1
            total_size += size
        
            if file_count >= config["max_files"]:
                break

    except OSError as error:
        print(f"Error: could not scan '{source}': {error}",
              file=sys.stderr)
        return None
    
    return file_count, total_size

def format_size(size_bytes: int) -> str:
    if size_bytes < BYTES_PER_KB:
        return f"{size_bytes} bytes"

    if size_bytes < BYTES_PER_MB:
        return f"{size_bytes / BYTES_PER_KB:.1f} KB"

    if size_bytes < BYTES_PER_GB:
        return f"{size_bytes / BYTES_PER_MB:.1f} MB"

    return f"{size_bytes / BYTES_PER_GB:.1f} GB"

def print_report(
        config: AppConfig,
        file_count: int,
        total_size: int,
        ) -> None:
    print("\n--- File Report ---")
    print(f"Source: {config['source_folder']}")
    print(f"Recursive: {config['recursive']}")
    print(f"Extensions: {config['extensions']}")
    print(f"Maximum files: {config['max_files']}")
    print(f"Matching files: {file_count}")
    print(f"Total size: {format_size(total_size)}")
    
def main() -> int:
    args = parse_arguments()

    config_path = Path(
        "03_cli_and_config/lesson_10_config.json"
    )

    config = load_config(
        config_path
    )

    if config is None:
        return EXIT_INVALID_INPUT

    source_folder = resolve_source_folder(
        args.source,
        config,
    )

    if source_folder is None:
        return EXIT_INVALID_INPUT

    recursive = resolve_recursive(
        args.recursive,
        config,
    )

    if recursive is None:
        return EXIT_INVALID_INPUT

    max_files = resolve_max_files(
        args.max_files,
        config
    )

    if max_files is None:
        return EXIT_INVALID_INPUT

    extensions = resolve_extensions(
        config
    )

    if extensions is None:
        return EXIT_INVALID_INPUT

    app_config = create_app_config(
            source_folder,
            recursive,
            max_files,
            extensions,
        )

    result = count_matching_files(app_config)
    if result is None:
        return EXIT_OPERATION_ERROR

    file_count, total_size = result
    print_report(app_config, file_count, total_size)

    return EXIT_SUCCESS

if __name__ == "__main__":
    sys.exit(main())    