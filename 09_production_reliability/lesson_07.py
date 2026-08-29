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

def run_operation(server):
    logging.info("Running operation on %s", server)
    return True

def main():
    setup_logging()

    try:
        server = validate_server("prod-server-01")
        result = run_operation(server)

        logging.info("Final result: %s", result)

    except ValueError as error:
        logging.error("Invalid configuration: %s", error)


if __name__ == "__main__":
    main()