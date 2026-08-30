
import sys
from pathlib import Path
from unittest.mock import patch

MODULE_DIR = Path(__file__).resolve().parents[1] / "10_production_automation"
sys.path.insert(0, str(MODULE_DIR))

from health import check_api_with_retry
from reporting import build_report, print_health_report
from capstone import main

@patch("health.check_api_health")
def test_retry_then_success(mock_check):
    mock_check.side_effect = [
    {
        "status": "CHECK_FAILED",
        "status_code": None,
        "error": "temporary failure",
    },
    {
        "status": "CHECK_FAILED",
        "status_code": None,
        "error": "temporary failure",
    },
    {
        "status": "HEALTHY",
        "status_code": 200,
        "error": None,
    },
]
    result = check_api_with_retry(
    "https://example.com",
    5,
    3,
)

    assert result["status"] == "HEALTHY"
    assert result["attempts"] == 3
    assert mock_check.call_count == 3

@patch("health.check_api_health")
def test_retry_exhaustion(mock_check):
    mock_check.side_effect = [
        {
            "status": "CHECK_FAILED",
            "status_code": None,
            "error": "temporary failure",
        },
        {
            "status": "CHECK_FAILED",
            "status_code": None,
            "error": "temporary failure",
        },
        {
            "status": "CHECK_FAILED",
            "status_code": None,
            "error": "temporary failure",
        },
    ]

    result = check_api_with_retry(
        "https://example.com",
        5,
        3,
    )

    assert result["status"] == "CHECK_FAILED"
    assert result["attempts"] == 3
    assert mock_check.call_count == 3

@patch("health.check_api_health")
def test_unhealthy_does_not_retry(mock_check):
    mock_check.return_value = {
        "status": "UNHEALTHY",
        "status_code": 404,
        "error": None,
    }

    result = check_api_with_retry(
        "https://example.com",
        5,
        3,
    )

    assert result["status"] == "UNHEALTHY"
    assert result["status_code"] == 404
    assert result["attempts"] == 1
    assert mock_check.call_count == 1




def test_build_report_healthy():
    system_info = {
        "hostname": "Javi_G",
        "system": "Windows",
        "release": "11",
    }
    process_result = {
        "process_name": "Code.exe",
        "status": "RUNNING",
        "error": None,
    }
    api_result = {
        "status": "HEALTHY",
        "status_code": 200,
        "error": None,
        "attempts": 1,
    }

    result = build_report("prod-server-01", system_info, process_result, api_result)

    assert result["overall_status"] == "HEALTHY"


def test_build_report_process_unhealthy():
    system_info = {
        "hostname": "Javi_G",
        "system": "Windows",
        "release": "11",
    }
    process_result = {
        "process_name": "Code.exe",
        "status": "NOT_RUNNING",
        "error": None,
    }
    api_result = {
        "status": "HEALTHY",
        "status_code": 200,
        "error": None,
        "attempts": 1,
    }

    result = build_report("prod-server-01", system_info, process_result, api_result)

    assert result["overall_status"] == "UNHEALTHY"


def test_build_report_api_unhealthy():
    system_info = {
        "hostname": "Javi_G",
        "system": "Windows",
        "release": "11",
    }
    process_result = {
        "process_name": "Code.exe",
        "status": "RUNNING",
        "error": None,
    }
    api_result = {
        "status": "UNHEALTHY",
        "status_code": 404,
        "error": None,
        "attempts": 1,
    }

    result = build_report("prod-server-01", system_info, process_result, api_result)

    assert result["overall_status"] == "UNHEALTHY"


def test_build_report_preserves_data():
    system_info = {
        "hostname": "Javi_G",
        "system": "Windows",
        "release": "11",
    }
    process_result = {
        "process_name": "Code.exe",
        "status": "RUNNING",
        "error": None,
    }
    api_result = {
        "status": "HEALTHY",
        "status_code": 200,
        "error": None,
        "attempts": 1,
    }

    result = build_report("prod-server-01", system_info, process_result, api_result)

    assert result["server"] == "prod-server-01"
    assert result["system"] == system_info
    assert result["process"] == process_result
    assert result["api"] == api_result

def test_print_health_report(capsys):
    
    system_info = {
        "hostname": "Javi_G",
        "system": "Windows",
        "release": "11",
    }
    process_result = {
        "process_name": "Code.exe",
        "status": "RUNNING",
        "error": None,
    }
    api_result = {
        "status": "HEALTHY",
        "status_code": 200,
        "error": None,
        "attempts": 1,
    }

    report = build_report("prod-server-01", system_info, process_result, api_result)

    
    print_health_report(report)

    
    captured = capsys.readouterr()
    output = captured.out

    assert "prod-server-01" in output
    assert "Process Status: RUNNING" in output
    assert "Overall Status: HEALTHY" in output


@patch("capstone.check_api_with_retry")
@patch("capstone.check_process")
@patch("capstone.get_system_info")
@patch("capstone.validate_config")
@patch("capstone.get_config")
@patch("capstone.configure_logging")
def test_main_stops_on_invalid_config(
    mock_logging,
    mock_get_config,
    mock_validate,
    mock_system,
    mock_process,
    mock_api,
):
    mock_get_config.return_value = {
        "server_name": "prod-server-01",
        "process_name": "Code.exe",
        "api_url": "https://api.github.com",
        "timeout": 5,
        "max_attempts": 3,
    }

    mock_validate.return_value = False

    main()

    mock_system.assert_not_called()
    mock_process.assert_not_called()
    mock_api.assert_not_called()

@patch("capstone.print_health_report")
@patch("capstone.build_report")
@patch("capstone.check_api_with_retry")
@patch("capstone.check_process")
@patch("capstone.get_system_info")
@patch("capstone.validate_config")
@patch("capstone.get_config")
@patch("capstone.configure_logging")
def test_main_runs_health_workflow(
    mock_logging,
    mock_get_config,
    mock_validate,
    mock_system,
    mock_process,
    mock_api,
    mock_build_report,
    mock_print_report,
):
    config = {
        "server_name": "prod-server-01",
        "process_name": "Code.exe",
        "api_url": "https://api.github.com",
        "timeout": 5,
        "max_attempts": 3,
    }

    system_info = {
        "hostname": "Javi_G",
        "system": "Windows",
        "release": "11",
    }

    process_result = {
        "process_name": "Code.exe",
        "status": "RUNNING",
        "error": None,
    }

    api_result = {
        "status": "HEALTHY",
        "status_code": 200,
        "error": None,
        "attempts": 1,
    }

    report = {
        "server": "prod-server-01",
        "system": system_info,
        "process": process_result,
        "api": api_result,
        "overall_status": "HEALTHY",
    }

    mock_get_config.return_value = config
    mock_validate.return_value = True
    mock_system.return_value = system_info
    mock_process.return_value = process_result
    mock_api.return_value = api_result
    mock_build_report.return_value = report

    main()

    mock_process.assert_called_once_with("Code.exe")

    mock_api.assert_called_once_with(
        "https://api.github.com",
        5,
        3,
    )

    mock_build_report.assert_called_once_with(
        "prod-server-01",
        system_info,
        process_result,
        api_result,
    )

    mock_print_report.assert_called_once_with(report)