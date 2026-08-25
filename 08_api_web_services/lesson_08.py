import os
import requests


BASE_URL = "https://api.github.com"
TOKEN = os.getenv("GITHUB_TOKEN")

def build_headers(token):
    headers = {
        "Accept": "application/vnd.github+json",
    }

    if token:
        headers["Authorization"] = f"Bearer {token}"

    return headers

headers = build_headers(TOKEN)


def api_get(endpoint, token=None, params=None):
    url = f"{BASE_URL}{endpoint}"
    headers = build_headers(token)

    try:
        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=10,
        )

        response.raise_for_status()
        return response.json()

    except requests.HTTPError as error:
        return {
            "error": True,
            "message": str(error),
        }

    except requests.RequestException as error:
        return {
            "error": True,
            "message": str(error),
        }

def summarize_repos(repos):
    return [
        {
            "name": repo.get("name", "Unknown"),
            "url": repo.get("html_url", "Unknown"),
        }
        for repo in repos
    ]

repos = api_get(
    "/users/javbds/repos",
    token=TOKEN,
    params={"per_page": 3},
)

if "error" not in repos:
    summaries = summarize_repos(repos)

    for repo in summaries:
        print(f"{repo['name']} -> {repo['url']}")
else:
    print(repos["message"])