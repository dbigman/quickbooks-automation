import sys
from pathlib import Path

# Ensure 'src' is importable
sys.path.insert(
    0, str(Path(__file__).resolve().parents[3] / "src"),
)

from quickbooks_autoreport.domain.settings import (  # noqa: E402
    Settings,
    VALID_INTERVALS,
)


def test_validate_defaults_ok():
    s = Settings()
    s.validate()


def test_get_interval_seconds_mapping():
    s = Settings(interval="5 minutes")
    assert s.get_interval_seconds() == 300
    s.interval = "15 minutes"
    assert s.get_interval_seconds() == 900
    s.interval = "30 minutes"
    assert s.get_interval_seconds() == 1800
    s.interval = "60 minutes"
    assert s.get_interval_seconds() == 3600


def test_invalid_interval_raises_value_error():
    s = Settings(interval="2 minutes")
    raised = False
    try:
        s.validate()
    except ValueError as e:
        raised = True
        assert "Invalid interval" in str(e)
        for opt in sorted(VALID_INTERVALS):
            assert opt in str(e)
    assert raised


def test_invalid_date_order_raises_value_error():
    s = Settings(
        report_date_from="2025-02-01",
        report_date_to="2025-01-31",
    )
    raised = False
    try:
        s.validate()
    except ValueError as e:
        raised = True
        assert "Start date" in str(e)
        assert "cannot be after" in str(e)
    assert raised


def test_invalid_date_format_raises_value_error():
    s = Settings(
        report_date_from="2025/01/01",
        report_date_to="2025-01-31",
    )
    raised = False
    try:
        s.validate()
    except ValueError as e:
        raised = True
        assert "Dates must be in YYYY-MM-DD format" in str(e)
    assert raised


def test_missing_company_file_raises_value_error(tmp_path):
    missing = tmp_path / "no_such_company.qbw"
    s = Settings(company_file=str(missing))
    raised = False
    try:
        s.validate()
    except ValueError as e:
        raised = True
        assert "does not exist" in str(e)
    assert raised


def test_ensure_output_directory_creates(tmp_path):
    out_dir = tmp_path / "sub"
    s = Settings(output_dir=str(out_dir))
    s.ensure_output_directory()
    assert out_dir.exists()
    assert out_dir.is_dir()