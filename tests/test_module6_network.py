import importlib.util
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
LESSON_PATH = PROJECT_ROOT / "06_network_automation" / "lesson_08.py"

spec = importlib.util.spec_from_file_location("lesson_08", LESSON_PATH)
lesson_08 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lesson_08)

def test_get_user_summary():
    data = {
        "login": "testuser",
        "public_repos": 5,
        "followers": 10,
        "html_url": "https://github.com/testuser",
    }

    result = lesson_08.get_user_summary(data)

    assert result["username"] == "testuser"
    assert result["public_repos"] == 5
    assert result["followers"] == 10

def test_fetch_json_success(monkeypatch):
    class FakeResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {"status": "ok"}

    def fake_get(url, timeout):
        return FakeResponse()

    monkeypatch.setattr(lesson_08.requests, "get", fake_get)

    result = lesson_08.fetch_json("https://example.com")

    assert result == {"status": "ok"} 

def test_fetch_json_failure(monkeypatch):
    def fake_get(url, timeout):
        raise lesson_08.requests.RequestException

    monkeypatch.setattr(lesson_08.requests, "get", fake_get)

    result = lesson_08.fetch_json("https://example.com")

    assert result is None