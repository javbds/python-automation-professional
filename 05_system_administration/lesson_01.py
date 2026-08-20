import subprocess

try:
    result = subprocess.run(
        ["whoami"],
        capture_output=True,
        text=True,
    )

    print(result.stdout.strip())
    print(f"Return code: {result.returncode}")
    print(f"Output: {result.stdout.strip()}")
    print(f"Error: {result.stderr.strip()}")

except FileNotFoundError:
    print("Command could not be found.")