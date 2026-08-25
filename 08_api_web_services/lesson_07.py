import os
import requests


def get_authenticated_user(token):
    url = "https://api.github.com/user"

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=10,
        )

        response.raise_for_status()
        return response.json()

    except requests.HTTPError:
        return {
            "error": True,
            "status": response.status_code,
            "message": "Authentication request failed.",
        }

    except requests.RequestException:
        return {
            "error": True,
            "message": "Network request failed.",
        }

token = os.getenv("GITHUB_TOKEN")

if token is None:
    print("GITHUB_TOKEN is not set.")
elif token == "your_token_here":
    print("Github token is only a placeholder.")
else:
    user = get_authenticated_user(token)

    if "error" not in user:
        print(f"Authenticated as: {user['login']}")
    else:
        print(user["message"])

headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json",
}