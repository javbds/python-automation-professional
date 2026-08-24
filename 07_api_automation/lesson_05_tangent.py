import requests


url = "https://jsonplaceholder.typicode.com/posts/1"

response = requests.get(url, timeout=5)
response.raise_for_status()

data = response.json()


def validate_post(data):
    if not isinstance(data, dict):
        return False, "Invalid response format."

    required_fields = ["userId", "id", "title"]

    for field in required_fields:
        if field not in data:
            return False, f"Missing expected field: {field}"

    title = data["title"]

    if not isinstance(title, str) or not title.strip():
        return False, "Invalid title value."

    return True, None

is_valid, error = validate_post(data)

if is_valid:
    print("Post ID:", data["id"])
    print("User ID:", data["userId"])
    print("Title:", data["title"])
else:
    print("Validation failed:", error)