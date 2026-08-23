import socket


def get_host_info():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    return {
        "hostname": hostname,
        "ip_address": ip_address,
    }


def main():
    host_info = get_host_info()

    print("--- Network Information ---")
    print(f"Hostname: {host_info['hostname']}")
    print(f"IP Address: {host_info['ip_address']}")


if __name__ == "__main__":
    main()