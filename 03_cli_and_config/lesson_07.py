from pathlib import Path
from typing import TypedDict

class AppConfig(TypedDict):
    source_folder: Path
    recursive: bool
    max_files: int

def print_config(
    config: AppConfig,
) -> None:
    print("\n--- Configuration ---")
    print( f"Source folder: {config['source_folder']}")
    print(f"Recursive: {config['recursive']}")
    print(f"Max files: {config['max_files']}")
    

def build_config(
    source_folder: Path,
    recursive: bool,
    max_files: int,
) -> AppConfig:

    config: AppConfig = {
        "source_folder": source_folder,
        "recursive": recursive,
        "max_files": max_files,
    }

    return config

def create_app_config(
    source_folder: Path,
    recursive: bool,
    max_files: int,
) -> AppConfig:
    return {
        "source_folder": source_folder,
        "recursive": recursive,
        "max_files": max_files,
    }

def main() -> None:
    source_folder = Path(
        "03_cli_and_config/cli_test"
    )

    recursive = False
    max_files = 100

    config = create_app_config(
        source_folder,
        recursive,
        max_files,
    )

    print_config(
        config
    )


if __name__ == "__main__":
    main()