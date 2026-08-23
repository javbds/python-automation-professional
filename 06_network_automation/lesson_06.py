import requests


def fetch_url(url):
    try:
        return requests.get(url, timeout=5)

    except requests.RequestException:
        return None

def main():
    url = "https://github.com"

    response = fetch_url(url)

    if response is None:
        print("Request failed.")
    else:
        print(f"Status Code: {response.status_code}")
        print(f"Reason: {response.reason}")


if __name__ == "__main__":
    main()