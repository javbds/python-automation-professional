import os

def get_environment_value(
        name: str,
        default: str | None = None,
    ) -> str | None:
    return os.getenv(name, default)

def main():
    mode = get_environment_value(
        "AUTOMATION_MODE",
        "development",
    )

    if mode is None:
        print("AUTOMATION_MODE was not found.")
        return

    print(f"Automation mode: {mode}")

if __name__ == "__main__":
    main()