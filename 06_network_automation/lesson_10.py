import requests


def check_service(name, url):
    try:
        response = requests.get(url, timeout=5)

        return {
            "name": name,
            "url": url,
            "status_code": response.status_code,
            "healthy": response.ok,
        }

    except requests.RequestException:
        return {
            "name": name,
            "url": url,
            "status_code": None,
            "healthy": False,
        }

def build_health_report():
    services = [
        ("GitHub", "https://github.com"),
        ("GitHub API", "https://api.github.com"),
    ]

    report = []

    for name, url in services:
        result = check_service(name, url)
        report.append(result)

    return report

def main():
    report = build_health_report()

    print("--- Network Health Report ---")

    for service in report:
        if service["healthy"]:
            status = "HEALTHY"
        else:
            status = "UNHEALTHY"

        print(
            f"{service['name']}: "
            f"{status} "
            f"(HTTP {service['status_code']})"
        )


if __name__ == "__main__":
    main()