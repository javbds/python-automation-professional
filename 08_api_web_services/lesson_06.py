import requests


def fetch_data(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response

    except requests.ConnectionError:
        print("Connection failed.")
        return None

    except requests.Timeout:
        print("Request timed out.")
        return None

    except requests.HTTPError as error:
        print(f"HTTP error: {error}")
        return None

    except requests.RequestException as error:
        print(f"Request failed: {error}")
        return None

response = fetch_data("https://api.github.com/")

if response is not None:
    print(f"Status: {response.status_code}")
else:
    print("No response received.")