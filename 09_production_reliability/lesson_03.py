import logging


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s: %(message)s"
    )


def main():
    setup_logging()

    server = "prod-server-01"

    logging.info("Automation started")
    logging.info(f"Target server: {server}")

    if server.startswith("prod"):
        logging.warning("Production server detected")

    logging.info("Automation completed")


if __name__ == "__main__":
    main()