import requests


def create_post(title, body, user_id):
    url = "https://jsonplaceholder.typicode.com/posts"

    payload = {
        "title": title,
        "body": body,
        "userId": user_id,
    }

    response = requests.post(url, json=payload, timeout=10)

    if response.ok:
        return response.json()

    return {
        "error": True,
        "status": response.status_code,
    }


post = create_post(
    "Second Test",
    "Different payload.",
    42,
)

if "error" not in post:
    print(f"Created ID: {post['id']}")
    print(f"Title: {post['title']}")
else:
    print(f"Request failed: {post['status']}")