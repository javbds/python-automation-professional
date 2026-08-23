import requests


def fetch_url(url):
    return requests.get(url)

def get_status(response):
    if response.status_code == 200:
        return "SUCCESS"

    return "FAILED"

def main():
    url = "https://github.com/"

    response = fetch_url(url)

    status = get_status(response)


    print(f"Result: {status}")
    print(f"URL: {url}")
    print(f"Status Code: {response.status_code}")
    print(f"Reason: {response.reason}")


if __name__ == "__main__":
    main()