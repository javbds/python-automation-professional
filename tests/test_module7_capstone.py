import importlib.util
from pathlib import Path
from unittest.mock import patch


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = PROJECT_ROOT / "07_api_automation" / "capstone.py"

spec = importlib.util.spec_from_file_location(
    "module7_capstone",
    MODULE_PATH
)
capstone = importlib.util.module_from_spec(spec)
spec.loader.exec_module(capstone)

def test_validate_post_valid():
    post = {
        "userId": 3,
        "id": 21,
        "title": "Automation test"
    }

    is_valid, error = capstone.validate_post(post)

    assert is_valid is True
    assert error is None

def test_validate_post_missing_title():
    post = {
        "userId": 3,
        "id": 21,
        
    }

    is_valid, error = capstone.validate_post(post)

    assert is_valid is False
    assert error ==  "Missing field: title"

def test_validate_post_invalid_title():
    post = {
        "userId": 3,
        "id": 21,
        "title": None
    }

    is_valid, error = capstone.validate_post(post)

    assert is_valid is False
    assert error == "Invalid title."

def test_build_post_report_counts():
    posts = [
        {
            "userId": 3,
            "id": 21,
            "title": "Valid post"
        },
        {
            "userId": 3,
            "id": 22
        }
    ]

    report = capstone.build_post_report(posts)

    assert report["total_count"] == 2
    assert len(report["valid_posts"]) == 1
    assert report["invalid_count"] == 1

def test_main_success(capsys):
    fake_posts = [
        {
            "userId": 3,
            "id": 21,
            "title": "First test post"
        },
        {
            "userId": 3,
            "id": 22,
            "title": "Second test post"
        }
    ]

    with patch.object(
        capstone,
        "get_api_data",
        return_value=fake_posts
    ):
        capstone.main()

    output = capsys.readouterr().out

    assert "User ID: 3" in output
    assert "Total posts: 2" in output
    assert "Valid posts: 2" in output
    assert "Invalid posts: 0" in output