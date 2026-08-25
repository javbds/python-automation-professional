from unittest.mock import patch

from importlib import import_module


capstone = import_module("08_api_web_services.capstone")

def test_build_headers_without_token():
    headers = capstone.build_headers()

    assert headers["Accept"] == "application/vnd.github+json"
    assert "Authorization" not in headers

def test_build_headers_with_token():
    headers = capstone.build_headers("fake-token")

    assert headers["Authorization"] == "Bearer fake-token"

def test_normalize_repo():
    repo = {
        "name": "python-automation-professional",
        "html_url": "https://example.com/repo",
        "private": False,
        "language": "Python",
    }

    result = capstone.normalize_repo(repo)

    assert result["name"] == "python-automation-professional"
    assert result["language"] == "Python"
    assert result["private"] is False

def test_normalize_repo_defaults():
    result = capstone.normalize_repo({})

    assert result["name"] == "Unknown"
    assert result["url"] == "Unknown"
    assert result["private"] is False
    assert result["language"] == "Unknown"

def test_fetch_all_repos_pagination():
    page_one = [
        {"name": "repo-one"},
        {"name": "repo-two"},
    ]

    page_two = [
        {"name": "repo-three"},
    ]

    with patch.object(
        capstone,
        "api_get",
        side_effect=[page_one, page_two, []],
    ):
        repos = capstone.fetch_all_repos("test-user")

    assert len(repos) == 3
    assert repos[0]["name"] == "repo-one"
    assert repos[2]["name"] == "repo-three"

def test_fetch_all_repos_api_error():
    fake_error = {
        "error": True,
        "message": "Simulated API failure.",
    }

    with patch.object(
        capstone,
        "api_get",
        return_value=fake_error,
    ):
        result = capstone.fetch_all_repos("test-user")

    assert result["error"] is True
    assert result["message"] == "Simulated API failure."

def test_build_report():
    repos = [
        {
            "name": "repo-one",
            "html_url": "https://example.com/one",
            "private": False,
            "language": "Python",
        },
        {
            "name": "repo-two",
            "html_url": "https://example.com/two",
            "private": True,
            "language": None,
        },
    ]

    report = capstone.build_report(repos)

    assert len(report) == 2
    assert report[0]["language"] == "Python"
    assert report[1]["language"] == "Unknown"

def test_main_success(capsys):
    fake_repos = [
        {
            "name": "repo-one",
            "html_url": "https://example.com/one",
            "private": False,
            "language": "Python",
        }
    ]

    with patch.object(
        capstone,
        "fetch_all_repos",
        return_value=fake_repos,
    ):
        capstone.main()

    output = capsys.readouterr().out

    assert "Repository Audit: javbds" in output
    assert "Total repositories: 1" in output
    assert "repo-one" in output

def test_main_api_error(capsys):
    fake_error = {
        "error": True,
        "message": "Simulated API failure.",
    }

    with patch.object(
        capstone,
        "fetch_all_repos",
        return_value=fake_error,
    ):
        capstone.main()

    output = capsys.readouterr().out

    assert "API error: Simulated API failure." in output