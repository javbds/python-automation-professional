import subprocess

from typing import NamedTuple

class CommandResult(NamedTuple):
    return_code: int
    output: str
    error: str

def run_command(command: list[str],) -> CommandResult | None:
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
        return None

def command_succeded(return_code: int) -> bool:
    return return_code == 0


def main():
    result = run_command(["whoami"])

    if result is None:
        return

    if command_succeded(result.return_code):
        print("Command succeeded.")
        print(f"Output: {result.output}")
    else:
        print("Command failed.")
        print(f"Error: {result.error}")

if __name__ == "__main__":
    main()