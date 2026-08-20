import subprocess

def run_command(command: list[str],) -> tuple[int, str, str] | None:
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
        )

        return (
            result.returncode,
            result.stdout.strip(),
            result.stderr.strip(),
        ) 

    except FileNotFoundError:
        print("Command could not be found.")
        return None


def main():
    result = run_command(["whoami"])

    if result is None:
        return

    return_code, output, error = result

    print(f"Return code: {return_code}")
    print(f"Output: {output}")
    print(f"Error: {error}")

if __name__ == "__main__":
    main()