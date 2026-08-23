import socket


def resolve_hostname(hostname):
    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror:
        return None
    
def main():
    hostname = "github.com"

    ip_address = resolve_hostname(hostname)

    print(f"Hostname: {hostname}")

    if ip_address is None:
        print("DNS resolution failed.")
    else:
        print(f"IP Address: {ip_address}")

if __name__ == "__main__":
    main()