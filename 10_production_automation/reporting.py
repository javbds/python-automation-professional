def build_report(
    server_name: str,
    system_info: dict,
    process_result: dict,
    api_result: dict,
) -> dict:
    if process_result["status"] == "RUNNING" and api_result["status"] == "HEALTHY":
        overall_status = "HEALTHY"
    else:
        overall_status = "UNHEALTHY"

    return {
        "server": server_name,
        "system": system_info,
        "process": process_result,
        "api": api_result,
        "overall_status": overall_status,
    }

def print_health_report(report: dict) -> None:
    print("Production Health Report")
    print("-" * 25)
    print(f"Server: {report['server']}")
    print(f"System: {report['system']['system']} {report['system']['release']}")
    print(f"Hostname: {report['system']['hostname']}")
    print(f"Process: {report['process']['process_name']}")
    print(f"Process Status: {report['process']['status']}")
    print(f"API Status: {report['api']['status']}")
    print(f"Status Code: {report['api']['status_code']}")
    print(f"Attempts: {report['api']['attempts']}")
    print(f"Overall Status: {report['overall_status']}")

