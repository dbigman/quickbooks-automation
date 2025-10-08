import sys
from datetime import datetime
from pathlib import Path
from typing import Optional
from typing import Optional
from typing import Optional
from typing import Optional

# Ensure 'src' is importable
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))

from quickbooks_autoreport.domain.report_result import (  # noqa: E402
    ReportResult,
)


def make_result(
    error: Optional[str] = None,
    changed: bool = True,
) -> ReportResult:
    return ReportResult(
        report_key="open_sales_orders",
        report_name="Open Sales Orders by Item",
        rows=150,
        changed=changed,
        timestamp=datetime(2025, 1, 31, 12, 0, 0),
        excel_created=True,
        insights={"total_value": 50000},
        connect_info={"version": "16.0", "company": "Gasco"},
        error=error,
    )


def test_success_true_when_no_error():
    rr = make_result(error=None)
    assert rr.success is True


def test_success_false_when_error():
    rr = make_result(error="Something went wrong")
    assert rr.success is False


def test_to_dict_contains_expected_fields_and_iso_timestamp():
    rr = make_result()
    d = rr.to_dict()

    # Required keys exist
    for key in [
        "report_key",
        "report_name",
        "rows",
        "changed",
        "timestamp",
        "excel_created",
        "insights",
        "connect_info",
        "error",
        "success",
    ]:
        assert key in d, f"Missing key: {key}"

    # Timestamp is ISO formatted
    assert d["timestamp"] == "2025-01-31T12:00:00"

    # Success mirrors property
    assert d["success"] == rr.success


def test_get_summary_for_success_changed_with_excel():
    rr = make_result(error=None, changed=True)
    summary = rr.get_summary()
    assert "✅ Changed" in summary
    assert "Open Sales Orders by Item" in summary
    assert "(150 rows)" in summary
    assert "📊 Excel created" in summary


def test_get_summary_for_success_unchanged_no_excel():
    rr = ReportResult(
        report_key="profit_loss",
        report_name="Profit & Loss",
        rows=0,
        changed=False,
        timestamp=datetime(2025, 1, 31, 12, 0, 0),
        excel_created=False,
        insights=None,
        connect_info={},
        error=None,
    )
    summary = rr.get_summary()
    assert "⚪ Unchanged" in summary
    assert "📊 Excel created" not in summary


def test_get_summary_for_error_contains_message():
    rr = make_result(error="Generation failed due to COM error")
    summary = rr.get_summary()
    assert summary.startswith("❌ ")
    assert "Generation failed due to COM error" in summary