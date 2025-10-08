import sys
from pathlib import Path

# Ensure 'src' is importable
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))

from quickbooks_autoreport.domain.diagnostics import (  # noqa: E402
    DiagnosticResult,
)


def make_diag(
    qb_status: str = "OK",
    sdk_status: str = "OK",
    conn_status: str = "OK",
):
    return DiagnosticResult(
        timestamp="2025-01-31T12:00:00",
        system_info={"os": "Windows 10", "python": "3.11"},
        quickbooks_installation={"status": qb_status, "version": "2023"},
        sdk_installation={"status": sdk_status, "version": "16.0"},
        connectivity_test={"status": conn_status, "message": "All good"},
        recommendations=["Install SDK", "Run as admin"],
    )


def test_to_dict_contains_expected_keys():
    d = make_diag().to_dict()
    for key in [
        "timestamp",
        "system_info",
        "quickbooks_installation",
        "sdk_installation",
        "connectivity_test",
        "recommendations",
    ]:
        assert key in d, f"Missing key in dict: {key}"


def test_get_summary_contains_sections():
    diag = make_diag(
        qb_status="OK",
        sdk_status="OK",
        conn_status="OK",
    )
    s = diag.get_summary()
    assert "=== QuickBooks Auto Reporter Diagnostics ===" in s
    assert "System Information:" in s
    assert "QuickBooks Installation:" in s
    assert "SDK Installation:" in s
    assert "Connectivity Test:" in s


def test_has_issues_true_when_any_not_ok():
    # QB error only
    diag = make_diag(qb_status="ERROR", sdk_status="OK", conn_status="OK")
    assert diag.has_issues() is True

    # SDK error only
    diag = make_diag(qb_status="OK", sdk_status="ERROR", conn_status="OK")
    assert diag.has_issues() is True

    # Connectivity error only
    diag = make_diag(qb_status="OK", sdk_status="OK", conn_status="ERROR")
    assert diag.has_issues() is True


def test_has_issues_false_when_all_ok():
    diag = make_diag(qb_status="OK", sdk_status="OK", conn_status="OK")
    assert diag.has_issues() is False


def test_get_error_count_counts_non_ok_statuses():
    # 0 errors
    diag = make_diag(qb_status="OK", sdk_status="OK", conn_status="OK")
    assert diag.get_error_count() == 0

    # 1 error
    diag = make_diag(qb_status="ERROR", sdk_status="OK", conn_status="OK")
    assert diag.get_error_count() == 1

    # 2 errors
    diag = make_diag(qb_status="ERROR", sdk_status="WARN", conn_status="OK")
    assert diag.get_error_count() == 2

    # 3 errors
    diag = make_diag(qb_status="ERROR", sdk_status="ERROR", conn_status="FAIL")
    assert diag.get_error_count() == 3