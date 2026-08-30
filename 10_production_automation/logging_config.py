import logging


def configure_logging() -> None:
    logging.basicConfig(
        filename="production_health.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

