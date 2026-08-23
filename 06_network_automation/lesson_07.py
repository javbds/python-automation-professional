import requests


def fetch_json(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()

        return response.json()

    except requests.RequestException:
        return None

def main():
    url = "https://api.github.com"

    data = fetch_json(url)

    if data is None:
        print("API request failed.")
    else:
        print(f"Current User URL: {data['current_user_url']}")
        print(f"Repository Search URL: {data['repository_search_url']}")


if __name__ == "__main__":
    main()