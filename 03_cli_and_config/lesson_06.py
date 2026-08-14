from pathlib import Path


DEFAULT_RECURSIVE = False
DEFAULT_MAX_FILES = 100

def apply_defaults(
    config: dict,
) -> tuple[bool, int]:

    recursive = config.get(
        "recursive",
        DEFAULT_RECURSIVE,
    )

    max_files = config.get(
        "max_files",
        DEFAULT_MAX_FILES,
    )

    return recursive, max_files

def validate_settings(
    recursive: object,
    max_files: object,
) -> bool:

    if not isinstance(recursive, bool):
        print(
            "Error: 'recursive' must be a Boolean"
        )
        return False

    if not isinstance(max_files, int):
        print(
            "Error: 'max_files' must be an Integer."
        )
        return False

    if max_files <= 0:
        print(
            "Error: 'max_files' must be greater than zero."
        )
        return False

    return True

def get_required_source(
        config: dict,
) -> Path | None:

    source_value = config.get(
        "source_folder"
    )

    if source_value is None:
        print(
            "Error: required setting 'source_folder' is missing"
        )
        return None
    
    if not isinstance(source_value, str):
        print(
            "Error: 'source_folder' must be a string"
        )
        return None

    source_folder = Path(
        source_value
    ).expanduser()

    if not source_folder.exists():
        print(
            f"Error: '{source_folder}' doesn't exist."
        )
        return None

    if not source_folder.is_dir():
        print(
            f"Error: '{source_folder}' is not a folder."
        )
        return None

    return source_folder
    
def main() -> None:
    config = {
        "source_folder": "03_cli_and_config/cli_test",
        "recursive": True,
        "max_files":25,
    }

    source_folder = get_required_source(
        config
    )

    if source_folder is None:
        return
    
    recursive, max_files = apply_defaults(
        config
    )

    if not validate_settings(
        recursive,
        max_files,
    ):
        return

    print(f"Source folder: {source_folder}")
    print(f"Recursive: {recursive}")
    print(f"Max Files: {max_files}")

if __name__ == "__main__":
    main()