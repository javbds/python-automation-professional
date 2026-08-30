import logging

from config import get_config, validate_config
from health import get_system_info, check_process, check_api_with_retry
from reporting import build_report, print_health_report
from logging_config import configure_logging

import logging

from config import get_config, validate_config
from health import get_system_info, check_process, check_api_with_retry
from reporting import build_report, print_health_report
from logging_config import configure_logging


def main():
    configure_logging()

    config = get_config()

    if not validate_config(config):
        logging.error("Invalid configuration")
        return

    system_info = get_system_info()

    process_result = check_process(config["process_name"])

    api_result = check_api_with_retry(
        config["api_url"],
        config["timeout"],
        config["max_attempts"],
    )


    report = build_report(
        config["server_name"],
        system_info,
        process_result,
        api_result,
    )

    logging.info("Process %s status: %s",
             process_result["process_name"],
             process_result["status"])

    logging.info("API status: %s", api_result["status"])

    logging.info("Final result: %s", report["overall_status"])

    print_health_report(report)


if __name__ == "__main__":
    main()
    