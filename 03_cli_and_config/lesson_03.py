import json
from pathlib import Path

def load_config(
    config_path: Path,
) -> dict | None:
    """
    Load configuration data from a JSON file.
    Returns: 
        the config dict, or None if loading fails
    """
    try:
        with config_path.open(
            "r",
            encoding="utf-8",
        ) as file:
            config = json.load(file)

    except FileNotFoundError:
        print(
            f"Error: Config file '{config_path}' was not found."
        )
        return None

    except PermissionError:
        print(
            f"Error: Permission denied while reading '{config_path}'."
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
            f"Error: Could not read '{config_path}': {error}"
        )
        return None

    return config

def validate_config(
        config: dict,
) -> tuple[Path, bool, list[str]] | None:
    """
    Validate required configuration values.
    
    Returns:
        A tuple containing: validated source folder, recursive setting, and a list
        Returns None is validation fails
    """
    if "source_folder" not in config:
        print("Error: Missing 'source_folder' in config.")
        return None
    if "recursive" not in config:
        print("Error: Missing 'recursive' in config.")
        return None
    if "extensions" not in config:
        print("Error: Missing 'extensions' in config.")
        return None

    source_folder = Path(
        config["source_folder"]
    ).expanduser()

    recursive = config["recursive"]
    extensions = config["extensions"]

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
    if not isinstance(recursive, bool):
        print(
            "Error: 'recursive must be true or false."
        )
        return None

    if not isinstance(extensions, list):
        print(
            "Error: 'extensions' must be a list."
        )
        return None

    return (
        source_folder,
        recursive,
        extensions
    )

def count_matching_files(
        source_folder: Path,
        recursive: bool,
        extensions: list[str],
) -> int:
    """
    Count files matching the configured extensions.
    If recursive is True, include files in subfolders.
    """
    if recursive:
        items = source_folder.rglob("*")
    else:
        items = source_folder.iterdir()

    file_count = 0

    for item in items:
        if not item.is_file():
            continue

        if item.suffix.lower() not in extensions:
            continue

        file_count += 1

    return file_count
    
def main() -> None:
    config_path = Path(
        "03_cli_and_config/config.json"
    )

    config = load_config(
        config_path
    )

    if config is None:
        return

    validated = validate_config(
        config
    )

    if validated is None:
        return

    source_folder, recursive, extensions = validated

    file_count = count_matching_files(
        source_folder,
        recursive,
        extensions,
    )

    print(f"Matching files found: {file_count}")

if __name__ == "__main__":
    main()