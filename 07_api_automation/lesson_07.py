import requests


def get_api_data(url, params = None, headers=None):
    try:
        response = requests.get(url, params=params, headers=headers, timeout=5)
        response.raise_for_status()

        return response.json()

    except requests.exceptions.HTTPError as error:
        print("HTTP error:", error)
        return None

    except requests.exceptions.ConnectionError as error:
        print("Connection error:", error)
        return None

    except requests.exceptions.Timeout as error:
        print("Request timed out:", error)
        return None
    except requests.exceptions.JSONDecodeError as error:
        print("Invalid JSON response:", error)
        return None

def main():
    url = "https://httpbin.org/headers"

    headers = {
        "X-Lesson": "Module-7"
    }

    data = get_api_data(url, headers=headers)

    if data is not None:
        print("Sent header:", data["headers"]["X-Lesson"])

if __name__ == "__main__":
    main()