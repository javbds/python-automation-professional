import requests


def get_api_data(url, params=None, headers=None):
    try:
        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=5
        )
        response.raise_for_status()

        return response.json()

    except requests.exceptions.HTTPError as error:
        print("HTTP error:", error)
        return None

    except requests.exceptions.ConnectionError as error:
        print("Connection error:", error)
        return None

    except requests.exceptions.Timeout as error:
        print("Request timed out:", error)
        return None

    except requests.exceptions.JSONDecodeError as error:
        print("Invalid JSON response:", error)
        return None

def validate_post(post):
    if not isinstance(post, dict):
        return False, "Post must be a dictionary."

    required_fields = ["userId", "id", "title"]

    for field in required_fields:
        if field not in post:
            return False, f"Missing field: {field}"

    if not isinstance(post["title"], str) or not post["title"].strip():
        return False, "Invalid title."

    return True, None

def build_post_report(posts):
    valid_posts = []
    invalid_count = 0

    for post in posts:
        is_valid, error = validate_post(post)

        if is_valid:
            valid_posts.append(post)
        else:
            invalid_count += 1

    return {
        "valid_posts": valid_posts,
        "invalid_count": invalid_count,
        "total_count": len(posts),
    }

def main():
    url = "https://jsonplaceholder.typicode.com/posts"

    user_id = 3

    params = {
        "userId": user_id
    }

    data = get_api_data(url, params=params)

    if data is None:
        print("Failed to retrieve.")
        return
    if not isinstance(data, list):
        print("Invalid API response format.")
        return
    
    report = build_post_report(data)

    print("User ID:", user_id)
    print("Total posts:", report["total_count"])
    print("Valid posts:", len(report["valid_posts"]))
    print("Invalid posts:", report["invalid_count"])


if __name__ == "__main__":
    main()