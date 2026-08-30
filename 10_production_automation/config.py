def get_config():
    config = {
        "server_name": "prod-server-01",
        "process_name": "Code.exe",
        "api_url": "https://api.github.com",
        "timeout": 5,
        "max_attempts": 3
    }
    return config

def validate_config(config):
    required_keys = ["server_name", "process_name", "api_url", "timeout", "max_attempts"]
    string_keys = ["server_name", "process_name", "api_url"]
    number_keys = ["timeout", "max_attempts"]

    for key in required_keys:
        if key not in config:
            return False

    for key in string_keys:
        value = config[key]
        if not isinstance(value, str) or not value.strip():
            return False

    for key in number_keys:
        value = config[key]
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            return False
        if value <= 0:
            return False

    return True