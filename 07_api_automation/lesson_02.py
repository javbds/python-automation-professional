import requests


url = "https://jsonplaceholder.typicode.com/users/1"

response = requests.get(url)

print("Status code:", response.status_code)

data = response.json()

print("Name:", data["name"])
print("Email:", data["email"])
print("City:", data["address"]["city"])
print("Latitude:", data["address"]["geo"]["lat"])
print("Longitude:", data["address"]["geo"]["lng"])