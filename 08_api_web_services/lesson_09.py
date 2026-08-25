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
                "per_page": 3,
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

def build_repo_report(repos):
    report = []

    for repo in repos:
        report.append(
            {
                "name": repo.get("name", "Unknown"),
                "url": repo.get("html_url", "Unknown"),
                "private": repo.get("private", False),
            }
        )

    return report

repos = fetch_all_repos("javbds", TOKEN)

if isinstance(repos, dict) and repos.get("error"):
    print(repos["message"])
else:
    report = build_repo_report(repos)

    print(f"Total repositories: {len(report)}")

    for repo in report:
        print(
            f"{repo['name']} | "
            f"Private: {repo['private']} | "
            f"{repo['url']}"
        )