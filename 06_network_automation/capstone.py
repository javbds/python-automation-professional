import socket

import requests

def resolve_hostname(hostname):
    try:
        return socket.gethostbyname(hostname)

    except socket.gaierror:
        return None

def check_service(name, hostname, url):
    ip_address = resolve_hostname(hostname)

    if ip_address is None:
        return {
            "name": name,
            "hostname": hostname,
            "ip_address": None,
            "status_code": None,
            "healthy": False,
        }

    try:
        response = requests.get(url, timeout=5)

        return {
            "name": name,
            "hostname": hostname,
            "ip_address": ip_address,
            "status_code": response.status_code,
            "healthy": response.ok,
        }

    except requests.RequestException:
        return {
            "name": name,
            "hostname": hostname,
            "ip_address": ip_address,
            "status_code": None,
            "healthy": False,
        }

def build_report():
    services = [
        ("GitHub", "github.com", "https://github.com"),
        ("GitHub API", "api.github.com", "https://api.github.com"),
    ]

    report = []

    for name, hostname, url in services:
        result = check_service(name, hostname, url)
        report.append(result)

    return report

def main():
    report = build_report()

    print("--- Network Service Monitor ---")

    for service in report:
        if service["healthy"]:
            status = "HEALTHY"
        else:
            status = "UNHEALTHY"

        print(f"\n{service['name']}")
        print(f"  Hostname: {service['hostname']}")
        print(f"  IP Address: {service['ip_address']}")
        print(f"  HTTP Status: {service['status_code']}")
        print(f"  Status: {status}")


if __name__ == "__main__":
    main()