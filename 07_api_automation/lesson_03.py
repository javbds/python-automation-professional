import requests


url = "https://jsonplaceholder.typicode.com/posts"

params = {
    "userId": 3,
    "id": 999
}

response = requests.get(url, params=params)

print("Status code:", response.status_code)
print("Request URL:", response.url)

data = response.json()

print("Data type:", type(data))
print("Number of posts:", len(data))

if data:
    first_post = data[0]

    print("First post ID:", first_post["id"])
    print("First post title:", first_post["title"])
else:
    print("No matching posts found.")