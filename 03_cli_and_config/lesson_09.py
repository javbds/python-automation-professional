import argparse
import sys

from pathlib import Path

EXIT_SUCCESS = 0
EXIT_INVALID_INPUT = 2

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate a numeric processing limit."
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Maximum number of items to process.",
    )

    parser.add_argument(
        "--source",
        type=Path,
        default=Path("."),
        help="Source folder to process.",
    )

    return parser.parse_args()

def validate_limit(
    limit: int,
) -> bool:
    if limit <= 0:
        print("Error: limit must be greater than zero.",
              file=sys.stderr,
        )
              
        return False

    return True

def validate_source(
    source: Path,
) -> bool:

    if not source.exists():
        print(
            f"Error: source '{source}' does not exist.",
            file=sys.stderr,
        )
        return False

    if not source.is_dir():
        print(
            f"Error: source '{source}' is not a folder.",
            file=sys.stderr,
        )
        return False

    return True

def main() -> int:
    args = parse_arguments()

    if not validate_source(args.source):
        return EXIT_INVALID_INPUT
    
    if not validate_limit(args.limit):
        return EXIT_INVALID_INPUT

    print(f"Source: {args.source}")
    print(f"Processing limit: {args.limit}")
    print("Program completed succesfully.")
    return EXIT_SUCCESS

if __name__ == "__main__":
    sys.exit(main())