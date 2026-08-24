import requests


url = "https://jsonplaceholder.typicode.com/posts/1"

response = requests.get(url, timeout=5)
response.raise_for_status()

data = response.json()

def validate_post(data):
    if not isinstance(data, dict):
        print("Invalid response format.")
        return False
    required_fields = ["userId", "id", "title"]

    for field in required_fields:
        if field not in data:
            print("Missing expected field:", field)
            return False

    title = data["title"]

    if not isinstance(title, str) or not title.strip():
        print("Invalid title value.")
        return False

    return True

if validate_post(data):
    print("Post ID:", data["id"])
    print("User ID:", data["userId"])
    print("Title:", data["title"])