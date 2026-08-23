import importlib.util
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CAPSTONE_PATH = PROJECT_ROOT / "06_network_automation" / "capstone.py"

spec = importlib.util.spec_from_file_location("module6_capstone", CAPSTONE_PATH)
capstone = importlib.util.module_from_spec(spec)
spec.loader.exec_module(capstone)

def test_resolve_hostname_success(monkeypatch):
    def fake_gethostbyname(hostname):
        return "127.0.0.1"

    monkeypatch.setattr(
        capstone.socket,
        "gethostbyname",
        fake_gethostbyname,
    )

    result = capstone.resolve_hostname("example.com")

    assert result == "127.0.0.1"

def test_resolve_hostname_failure(monkeypatch):
    def fake_gethostbyname(hostname):
        raise capstone.socket.gaierror

    monkeypatch.setattr(
        capstone.socket,
        "gethostbyname",
        fake_gethostbyname,
    )

    result = capstone.resolve_hostname("bad.invalid")

    assert result is None

def test_check_service_success(monkeypatch):
    def fake_resolve(hostname):
        return "127.0.0.1"

    class FakeResponse:
        status_code = 200
        ok = True

    def fake_get(url, timeout):
        return FakeResponse()

    monkeypatch.setattr(
        capstone,
        "resolve_hostname",
        fake_resolve,
    )

    monkeypatch.setattr(
        capstone.requests,
        "get",
        fake_get,
    )

    result = capstone.check_service(
        "Example",
        "example.com",
        "https://example.com",
    )

    assert result["name"] == "Example"
    assert result["ip_address"] == "127.0.0.1"
    assert result["status_code"] == 200
    assert result["healthy"] is True

def test_check_service_dns_failure(monkeypatch):
    def fake_resolve(hostname):
        return None

    monkeypatch.setattr(
        capstone,
        "resolve_hostname",
        fake_resolve,
    )

    result = capstone.check_service(
        "Broken",
        "bad.invalid",
        "https://bad.invalid",
    )

    assert result["ip_address"] is None
    assert result["status_code"] is None
    assert result["healthy"] is False

def test_check_service_http_failure(monkeypatch):
    def fake_resolve(hostname):
        return "127.0.0.1"

    def fake_get(url, timeout):
        raise capstone.requests.RequestException

    monkeypatch.setattr(
        capstone,
        "resolve_hostname",
        fake_resolve,
    )

    monkeypatch.setattr(
        capstone.requests,
        "get",
        fake_get,
    )

    result = capstone.check_service(
        "Example",
        "example.com",
        "https://example.com",
    )

    assert result["ip_address"] == "127.0.0.1"
    assert result["status_code"] is None
    assert result["healthy"] is False