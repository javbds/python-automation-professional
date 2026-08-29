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


def main():
    setup_logging()

    server = "offline-server"

    try:
        
        result = connect_to_server(server)
        logging.info("Connection result: %s", result)

    except ConnectionError as error:
        logging.error("Connection failed: %s", error)


if __name__ == "__main__":
    main()