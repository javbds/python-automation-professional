import logging


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s: %(message)s"
    )


def connect_to_server(server):
    if server == "offline-server":
        raise ConnectionError(f"Could not connect to {server}")

    logging.info("Connected to %s", server)
    return True

def run_with_retry(server, max_attempts=3):
    for attempt in range(1, max_attempts + 1):
        try:
            return connect_to_server(server)

        except ConnectionError as error:
            logging.warning(
                "Attempt %s failed: %s",
                attempt,
                error
            )

    logging.error("All connection attempts failed")
    return False

def main():
    setup_logging()

    result = run_with_retry("prod-server-01")

    logging.info("Final result: %s", result)


if __name__ == "__main__":
    main()