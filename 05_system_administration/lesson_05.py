import platform

def get_system_info() -> dict[str, str]:
    return {
        "system": platform.system(),
        "release": platform.release(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "hostname": platform.node(),
    }

def is_windows(info: dict[str, str]) -> bool:
    return info["system"] == "Windows"

def main():
    info = get_system_info()

    print(f"System: {info['system']}")
    print(f"Release: {info['release']}")
    print(f"Machine: {info['machine']}")
    print(f"Processor: {info['processor']}")
    print(f"Hostname: {info['hostname']}")

    if is_windows(info):
        print("Windows system detected.")
    else:
        print("Non-Windows system detected.")

if __name__ == "__main__":
    main()