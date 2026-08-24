import os
import requests


url = "https://httpbin.org/headers"

api_token = os.getenv("API_TOKEN")

if not api_token:
    raise ValueError("API_TOKEN environment variable is required.")

headers = {
    "Authorization": f"Bearer {api_token}"
}

response = requests.get(url, headers=headers, timeout=5)
response.raise_for_status()

data = response.json()

print("Status code:", response.status_code)
print("Authorization header sent successfully.")