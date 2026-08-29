import os


def get_config():
    mode = os.getenv("AUTOMATION_MODE", "development")
    server = os.getenv("SERVER_NAME")

    if not server:
        raise ValueError("SERVER_NAME is required")

    return mode, server


def main():
    mode, server = get_config()
    print(f"Automation mode: {mode}")
    print(f"Server: {server}")

if __name__ == "__main__":
    main()