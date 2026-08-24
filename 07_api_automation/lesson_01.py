import requests


url = "https://jsonplaceholder.typicode.com/users/1"

response = requests.get(url)

print("Status code:", response.status_code)
print("Response:")
print(response.text)