import requests


def get_github_user(username):
    url = f"https://api.github.com/users/{username}"

    response = requests.get(url, timeout=10)

    if response.ok:
        return response.json()

    return {
        "error": True,
        "status": response.status_code,
        "message": response.json().get("message", "Unknown error"),
    }

user = get_github_user("javbds")

if "error" not in user:
    print(user["login"])
    print(user["public_repos"])
    print(f"Profile: {user['html_url']}")
else:
    print(f"Error {user['status']}: {user['message']}")