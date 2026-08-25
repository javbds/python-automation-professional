import requests


url = "https://api.github.com/users/javbds"

response = requests.get(url, timeout=10)

data = response.json()

print(f"Status: {response.status_code}")

if response.ok:
    print(f"Username: {data['login']}")
    print(f"Public repos: {data['public_repos']}")
    print(f"Hireable: {data['hireable']}")
else:
    print(f"Request failed: {data['message']}")