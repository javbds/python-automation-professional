import importlib.util
from pathlib import Path

import pytest
import os


MODULE_PATH = (
    Path(__file__).resolve().parents[1]
    / "09_production_reliability"
    / "lesson_07.py"
)

spec = importlib.util.spec_from_file_location("lesson_07", MODULE_PATH)
lesson_07 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lesson_07)

validate_server = lesson_07.validate_server

CAPSTONE_PATH = (
    Path(__file__).resolve().parents[1]
    / "09_production_reliability"
    / "capstone.py"
)

capstone_spec = importlib.util.spec_from_file_location("module9_capstone", CAPSTONE_PATH)
capstone = importlib.util.module_from_spec(capstone_spec)
capstone_spec.loader.exec_module(capstone)

def test_valid_server():
    result = validate_server("prod-server-01")

    assert result == "prod-server-01"

def test_missing_server():
    with pytest.raises(ValueError):
        validate_server("")

def test_invalid_server_prefix():
    with pytest.raises(ValueError):
        validate_server("random-server")

def test_missing_server_message():
    with pytest.raises(ValueError, match="Server name is required"):
        validate_server("")

def test_validate_config_success():
    server, attempts = capstone.validate_config("prod-server-01", 3)

    assert server == "prod-server-01"
    assert attempts == 3

def test_validate_config_missing_server():
    with pytest.raises(ValueError, match="SERVER_NAME is required"):
        capstone.validate_config(None, 3)

def test_validate_config_bad_attempts():
    with pytest.raises(ValueError, match="MAX_ATTEMPTS must be at least 1"):
        capstone.validate_config("prod-server-01", 0)

def test_run_with_retry_success():
    result = capstone.run_with_retry("prod-server-01", 3)

    assert result is True

def test_run_with_retry_failure():
    result = capstone.run_with_retry("prod-offline", 3)

    assert result is False