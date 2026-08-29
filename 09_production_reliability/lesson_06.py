import logging
import time


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s: %(message)s"
    )


def run_request(timeout):
    logging.info("Starting request")

    start_time = time.time()
    time.sleep(2)
    elapsed = time.time() - start_time

    if elapsed > timeout:
        raise TimeoutError(f"Request exceeded {timeout} seconds")

    logging.info("Request completed in %.2f seconds", elapsed)
    return True


def main():
    setup_logging()

    try:
        result = run_request(timeout=3)
        logging.info("Final result: %s", result)

    except TimeoutError as error:
        logging.error("Timeout: %s", error)


if __name__ == "__main__":
    main()