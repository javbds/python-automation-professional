import requests


url = "https://jsonplaceholder.typicode.com/posts/1"

response = requests.get(url)

try:
    response = requests.get(url, timeout=5)

    response.raise_for_status()

    data = response.json()
    print("Title:", data["title"])

except requests.exceptions.HTTPError as error:
    print("HTTP error:", error)

except requests.exceptions.ConnectionError as error:
    print("Connection error:", error)

except requests.exceptions.Timeout as error:
    print("Request timed out:", error)