from importlib import import_module
from unittest.mock import patch


lesson_10 = import_module(
    "05_system_administration.lesson_10"
)


def test_process_is_running():
    processes = """
    Code.exe
    python.exe
    explorer.exe
    """

    assert lesson_10.is_process_running(
        processes,
        "Code.exe",
    ) is True


def test_process_is_not_running():
    processes = """
    Code.exe
    python.exe
    explorer.exe
    """

    assert lesson_10.is_process_running(
        processes,
        "DefNotRun.exe",
    ) is False


def test_run_command_success():
    with patch.object(
        lesson_10.subprocess,
        "run",
    ) as mock_run:
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "fake output\n"
        mock_run.return_value.stderr = ""

        result = lesson_10.run_command(["fake-command"])

    assert result is not None
    assert result.return_code == 0
    assert result.output == "fake output"
    assert result.error == ""


def test_run_command_not_found():
    with patch.object(
        lesson_10.subprocess,
        "run",
        side_effect=FileNotFoundError,
    ):
        result = lesson_10.run_command(
            ["fake-command"]
        )

    assert result is None