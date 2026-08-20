import subprocess
import logging
import json


from pathlib import Path
from typing import NamedTuple


logging.basicConfig(
    filename="system_automation.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

class CommandResult(NamedTuple):
    return_code: int
    output: str
    error: str


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
        print("Command could not be found.")
        logging.error("Command could not be found: %s, command[0]")
        return None

def get_running_processes() -> str | None:
    result = run_command(["tasklist"])
        
    if result is None:
        return None

    if result.return_code != 0:
        print(f"Could not retrieve processes: {result.error}")
        logging.error("Could not retrieve processes: %s", result.error,)
        return None

    return result.output

def is_process_running(
    processes: str,
    process_name: str,
) -> bool:
    return process_name.lower() in processes.lower()

def load_process_config(config_path: Path) -> list[str]:
    with config_path.open("r", encoding="utf-8") as file:
        data = json.load(file)
    if "processes" not in data:
        print("Config error: 'processes' key is missing.")
        return []

    if not isinstance(data["processes"], list):
        print("Config error: 'processes' must be a list.")
        return []
    
    return data["processes"]

def main():
    config_path = Path(
        "05_system_administration/process_config.json"
    )

    process_names = load_process_config(config_path)


    processes = get_running_processes()

    if processes is None:
        return

    for process_name in process_names:
        if is_process_running(processes, process_name):
            print(f"{process_name} is running.")
            logging.info("Checked %s: running", process_name)
        else:
            print(f"{process_name} is not running.")
            logging.info("Checked %s: not running", process_name)


if __name__ == "__main__":
    main()