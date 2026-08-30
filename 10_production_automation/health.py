import platform
import subprocess
import requests

def get_system_info() -> dict[str, str]:
    return {
        "hostname" : platform.node(),
        "system" : platform.system(),
        "release": platform.release(),
    }

def is_windows(info: dict[str, str]) -> bool:
    return info["system"] == "Windows"

def check_process(process_name: str) -> dict[str, str | None]:
    try:
        result = subprocess.run(
            ["tasklist"],
            capture_output=True,
            text=True,
        )
    except FileNotFoundError as error:
        return {
            "process_name": process_name,
            "status": "CHECK_FAILED",
            "error": str(error),
        }

    if process_name.lower() in result.stdout.lower():
        status = "RUNNING"
    else:
        status = "NOT_RUNNING"

    return {
        "process_name": process_name,
        "status": status,
        "error": None,
    }

def check_api_health(
        api_url: str,
        timeout: int
) -> dict[str, str | int | None]:
    try:
        response = requests.get(api_url, timeout=timeout)
    except requests.RequestException as error:
        return {
            "status": "CHECK_FAILED",
            "status_code": None,
            "error": str(error),
        }

    if response.status_code == 200:
        status = "HEALTHY"
    else:
        status = "UNHEALTHY"

    return {
        "status": status,
        "status_code": response.status_code,
        "error": None
    }

def check_api_with_retry(
    api_url: str,
    timeout: int,
    max_attempts: int,
) -> dict[str, str | int | None]:
    for attempt in range(1, max_attempts + 1):
        result = check_api_health(api_url, timeout)

        if result["status"] in ("HEALTHY", "UNHEALTHY"):
            result["attempts"] = attempt
            return result

        if attempt == max_attempts:
            result["attempts"] = attempt
            return result

def main():
    info = get_system_info()

    print(f"System: {info['system']}")
    print(f"Release: {info['release']}")
    print(f"Hostname: {info['hostname']}")

    if is_windows(info):
        print("Windows system detected.")
    else:
        print("Non-Windows system detected.")

if __name__ == "__main__":
    main()