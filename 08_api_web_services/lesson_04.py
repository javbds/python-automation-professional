import requests


url = "https://api.github.com/users/javbds/repos"

for page in range(1, 4):
    params = {
        "per_page": 3,
        "page": page,
    }

    response = requests.get(url, params=params, timeout=10)

    if response.ok:
        repos = response.json()

        print(f"\nPage {page}")

        for repo in repos:
            print(repo["name"])
    else:
        print(f"Request failed: {response.status_code}")
        break