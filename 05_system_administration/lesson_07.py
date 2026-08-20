import subprocess
import logging

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
        logging.erro("Command could not be found: %s, command[0]")
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

def main():
    processes = get_running_processes()

    if processes is None:
        return

    process_name = input("Enter process name: ").strip()

    if not process_name:
        print("Process name cannot be empty.")
        logging.warning("Empty process name entered.")
        return
    
    if is_process_running(processes, process_name):
        print(f"{process_name} is running.")
        logging.info("Checked %s: running", process_name)
    else:
        print(f"{process_name} is not running.")
        logging.info("Checked %s: not running", process_name)


if __name__ == "__main__":
    main()