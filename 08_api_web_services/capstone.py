import os
import requests


BASE_URL = "https://api.github.com"
TOKEN = os.getenv("GITHUB_TOKEN")


def build_headers(token=None):
    headers = {
        "Accept": "application/vnd.github+json",
    }

    if token:
        headers["Authorization"] = f"Bearer {token}"

    return headers

def api_get(endpoint, token=None, params=None):
    url = f"{BASE_URL}{endpoint}"

    try:
        response = requests.get(
            url,
            headers=build_headers(token),
            params=params,
            timeout=10,
        )

        response.raise_for_status()
        return response.json()

    except requests.RequestException as error:
        return {
            "error": True,
            "message": str(error),
        }

def fetch_all_repos(username, token=None):
    all_repos = []
    page = 1

    while True:
        repos = api_get(
            f"/users/{username}/repos",
            token=token,
            params={
                "per_page": 5,
                "page": page,
            },
        )

        if isinstance(repos, dict) and repos.get("error"):
            return repos

        if not repos:
            break

        all_repos.extend(repos)
        page += 1

    return all_repos

def normalize_repo(repo):
    return {
        "name": repo.get("name", "Unknown"),
        "url": repo.get("html_url", "Unknown"),
        "private": repo.get("private", False),
        "language": repo.get("language") or "Unknown",
    }

def build_report(repos):
    return [normalize_repo(repo) for repo in repos]

def main():
    username = "javbds"

    repos = fetch_all_repos(username, TOKEN)

    if isinstance(repos, dict) and repos.get("error"):
        print(f"API error: {repos['message']}")
        return

    report = build_report(repos)

    print(f"Repository Audit: {username}")
    print(f"Total repositories: {len(report)}")

    for repo in report:
        print(
            f"{repo['name']} | "
            f"Language: {repo['language']} | "
            f"Private: {repo['private']}"
        )


if __name__ == "__main__":
    main()