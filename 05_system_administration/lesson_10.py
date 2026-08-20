import json
import logging
import platform
import subprocess

from pathlib import Path
from typing import NamedTuple

class CommandResult(NamedTuple):
    return_code: int
    output: str
    error: str

logging.basicConfig(
    filename="system_health.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def run_command(
    command: list[str],
) -> CommandResult | None:
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
        )

        return CommandResult(
            return_code=result.returncode,
            output=result.stdout.strip(),
            error=result.stderr.strip(),
        )

    except FileNotFoundError:
        logging.error(
            "Command could not be found: %s",
            command[0],
        )
        return None

def get_system_info() -> dict[str, str]:
    return {
        "hostname": platform.node(),
        "system": platform.system(),
        "release": platform.release(),
        "machine": platform.machine(),
        "processor": platform.processor(),
    }

def load_process_config(config_path: Path) -> list[str]:
    with config_path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if "processes" not in data:
        logging.error("Config error: 'processes' key is missing.")
        return []

    if not isinstance(data["processes"], list):
        logging.error("Config error: 'processes' must be a list.")
        return []

    return data["processes"]

def get_running_processes() -> str | None:
    result = run_command(["tasklist"])

    if result is None:
        return None

    if result.return_code != 0:
        logging.error(
            "Could not retrieve processes: %s",
            result.error,
        )
        return None

    return result.output

def is_process_running(
    processes: str,
    process_name: str,
) -> bool:
    return process_name.lower() in processes.lower()

def print_system_report(
    info: dict[str, str],
    process_names: list[str],
    processes: str,
) -> None:
    print("\n--- System Health Report ---")
    print(f"Hostname: {info['hostname']}")
    print(f"System: {info['system']} {info['release']}")
    print(f"Machine: {info['machine']}")
    print(f"Processor: {info['processor']}")

    print("\n--- Process Checks ---")

    for process_name in process_names:
        if is_process_running(processes, process_name):
            print(f"[RUNNING] {process_name}")
            logging.info("Checked %s: running", process_name)
        else:
            print(f"[NOT RUNNING] {process_name}")
            logging.info("Checked %s: not running", process_name)

def main():
    config_path = Path(
        "05_system_administration/system_config.json"
    )

    process_names = load_process_config(config_path)

    if not process_names:
        print("No processes configured.")
        return

    info = get_system_info()

    processes = get_running_processes()

    if processes is None:
        print("Could not retrieve running processes.")
        return

    print_system_report(
        info,
        process_names,
        processes,
    )

if __name__ == "__main__":
    main()