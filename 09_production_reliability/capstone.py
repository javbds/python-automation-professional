import logging
import os


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s: %(message)s"
    )


def get_config():
    server = os.getenv("SERVER_NAME")
    max_attempts = int(os.getenv("MAX_ATTEMPTS", "3"))

    return server, max_attempts

def validate_config(server, max_attempts):
    if not server:
        raise ValueError("SERVER_NAME is required")

    if not server.startswith(("dev-", "prod-")):
        raise ValueError("SERVER_NAME must begin with dev- or prod-")

    if max_attempts < 1:
        raise ValueError("MAX_ATTEMPTS must be at least 1")

    return server, max_attempts

def connect_to_server(server):
    if server == "prod-offline":
        raise ConnectionError(f"Could not connect to {server}")

    logging.info("Connected to %s", server)
    return True

def run_with_retry(server, max_attempts):
    for attempt in range(1, max_attempts + 1):
        try:
            return connect_to_server(server)

        except ConnectionError as error:
            logging.warning(
                "Attempt %s failed: %s",
                attempt,
                error
            )

    logging.error("All %s connection attempts failed", max_attempts)
    return False

def main():
    setup_logging()

    try:
        server, max_attempts = get_config()
        server, max_attempts = validate_config(server, max_attempts)

        result = run_with_retry(server, max_attempts)

        logging.info("Final result: %s", result)

    except ValueError as error:
        logging.error("Configuration error: %s", error)


if __name__ == "__main__":
    main()