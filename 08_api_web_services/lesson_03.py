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

def summarize_user(user):
    return {
        "username": user.get("login", "Unknown"),
        "name": user.get("name", "Unknown"),
        "location": user.get("location") or "Unknown",
        "public_repos": user.get("public_repos", 0),
    }

user = get_github_user("javbds")

if "error" not in user:
    summary = summarize_user(user)
    print(summary)
else:
    print(f"Error {user['status']}: {user['message']}")

profile = {
    "user": {
        "login": "javbds",
        "stats": {
            "repos": 9,
            "followers": 0,
        },
        
    }
}

print(profile["user"]["login"])
user_data = profile.get("user", {})
stats = user_data.get("stats", {})
repos = stats.get("repos", 0)

print(repos)