import importlib.util
from pathlib import Path
from unittest.mock import Mock, patch


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = PROJECT_ROOT / "07_api_automation" / "lesson_07.py"

spec = importlib.util.spec_from_file_location("lesson_07", MODULE_PATH)
lesson_07 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lesson_07)

get_api_data = lesson_07.get_api_data

def test_get_api_data_success():
    fake_response = Mock()

    fake_response.json.return_value = {
        "id": 1,
        "title": "Test post"
    }

    with patch.object(
        lesson_07.requests,
        "get",
        return_value=fake_response
    ):
        result = get_api_data("https://example.com/posts/1")

    assert result["id"] == 1
    assert result["title"] == "Test post"

def test_get_api_data_http_error():
    fake_response = Mock()
    fake_response.raise_for_status.side_effect = (
        lesson_07.requests.exceptions.HTTPError("404 Not Found")
    )

    with patch.object(
        lesson_07.requests,
        "get",
        return_value=fake_response
    ):
        result = get_api_data("https://example.com/missing")

    assert result is None

def test_get_api_data_connection_error():
    with patch.object(
        lesson_07.requests,
        "get",
        side_effect=lesson_07.requests.exceptions.ConnectionError(
            "Connection failed"
        )
    ):
        result = get_api_data("https://example.com")

    assert result is None

def test_get_api_data_timeout():
    with patch.object(
        lesson_07.requests,
        "get",
        side_effect=lesson_07.requests.exceptions.Timeout(
            "Request timed out"
        )
    ):
        result = get_api_data("https://example.com")

    assert result is None

def test_get_api_data_invalid_json():
    fake_response = Mock()
    fake_response.json.side_effect = (
        lesson_07.requests.exceptions.JSONDecodeError(
            "Invalid JSON",
            "",
            0
            )
    )

    with patch.object(
        lesson_07.requests,
        "get",
        return_value=fake_response
    ):
        result = get_api_data("https://example.com/")

    assert result is None