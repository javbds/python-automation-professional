import os

def get_environment_setting(
        name : str,
) -> str | None:
    """
    Retrieve one environment variable.
    Returns:
        a string or None if variable not availble"""

    return os.environ.get(name)

def get_max_files() -> int | None:
    """
    Retrieve and validate the MAX_FILES environment variable.
    """
    value = get_environment_setting(
        "MAX_FILES"
    )

    if value is None:
        print(
            "Error: MAX_FILES environment variable is not set."
        )
        return None

    try:
        max_files = int(value)

    except ValueError:
        print(
            "Error: MAX_FILES must be a whole number."
        )
        return None

    if max_files <= 0:
        print(
            "Error: MAX_FILES must be greater than zero."
        )
        return None

    return max_files

def main() -> None:
    max_files = get_max_files()

    if max_files is None:
        return

    print(f"Maximum files: {max_files}")
    print(f"Type: {type(max_files)}")

if __name__ == "__main__":
    main()