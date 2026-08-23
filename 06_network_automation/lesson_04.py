import requests


def fetch_url(url):
    return requests.get(url)

def main():
    url = "https://github.com"

    response = fetch_url(url)

    print(f"URL: {url}")
    print(f"Status Code: {response.status_code}")
    print(f"Reason: {response.reason}")
    print(f"Content Type: {response.headers.get('Content-Type')}")


if __name__ == "__main__":
    main()