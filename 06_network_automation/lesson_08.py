import requests


def fetch_json(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()

        return response.json()

    except requests.RequestException:
        return None

def get_user_summary(data):
    return {
        "username": data.get("login"),
        "public_repos": data.get("public_repos"),
        "followers": data.get("followers"),
        "profile_url": data.get("html_url"),
    }

def main():
    url = "https://api.github.com/users/javbds"

    data = fetch_json(url)

    if data is None:
        print("API request failed.")
        return

    summary = get_user_summary(data)

    print("--- GitHub User Summary ---")
    print(f"Username: {summary['username']}")
    print(f"Public Repositories: {summary['public_repos']}")
    print(f"Followers: {summary['followers']}")
    print(f"Profile: {summary['profile_url']}")


if __name__ == "__main__":
    main()