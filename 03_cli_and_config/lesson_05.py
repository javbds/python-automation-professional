import json
import os
import argparse
from pathlib import Path


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

def resolve_max_files(
          cli_value: int | None,
    config: dict,
) -> int | None:
    """
    Resolve max_files using:
    CLI > environment > JSON.
    """
    if cli_value is not None:
         if cli_value <= 0:
              print(
                   "error: --max-files must be greater than zero."
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
                  "Error: MAX_FILES environment variable must be a whole number."
             )
             return None

        if max_files <= 0:
             print(
                  "Error: MAX_FILES must be greater than zero."
             )
             return None

        return max_files
    
    json_value = config.get(
         "max_files"
    )

    if not isinstance(json_value, int):
        print(
            "Error: JSON 'max_files' must be an integer."
        )
        return None

    if json_value <= 0:
         print(
              "Error: JSON 'max_files' must be greater than zero."
         )
         return None

    return json_value

def parse_arguments() -> argparse.Namespace:
    """
    Parse optional command-line override
    """
    parser = argparse.ArgumentParser(
         description="Demonstrate configuration precedence."
    )

    parser.add_argument(
         "--max-files",
         type=int,
         help="Override the maximum number of files.",
    )

    return parser.parse_args()

def main() -> None:
        args = parse_arguments()

        config_path = Path(
            "03_cli_and_config/lesson_05_config.json"
        )

        config = load_config(
            config_path
        )

        if config is None:
            return

        app_mode = config.get(
            "app_mode"
        )

        max_files = resolve_max_files(
             args.max_files,
             config,
        )

        if max_files is None:
             return

        print(f"App mode: {app_mode}")
        print(f"Max files: {max_files}")

if __name__ == "__main__":
        main()