import logging


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s: %(message)s"
    )


def validate_server(server):
    if not server:
        raise ValueError("Server name is required")

    if not server.startswith(("dev-", "prod-")):
        raise ValueError("Server must begin with dev- or prod-")

    return server

def connect_to_server(server):
    if server == "prod-offline":
        raise ConnectionError(f"Could not connect to {server}")

    logging.info("Connected to %s", server)
    return True

def run_automation(server, max_attempts=3):
    server = validate_server(server)

    for attempt in range(1, max_attempts + 1):
        try:
            return connect_to_server(server)

        except ConnectionError as error:
            logging.warning(
                "Attempt %s failed: %s",
                attempt,
                error
            )

    logging.error("Automation failed after %s attempts", max_attempts)
    return False

def main():
    setup_logging()

    try:
        result = run_automation("prod-server-01")
        logging.info("Final result: %s", result)

    except ValueError as error:
        logging.error("Invalid configuration: %s", error)


if __name__ == "__main__":
    main()