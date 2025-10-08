import sys
from pathlib import Path
from unittest.mock import Mock

# Ensure 'src' is importable
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))

from quickbooks_autoreport.adapters.file_adapter import FileAdapter  # noqa: E402
from quickbooks_autoreport.services.insights_generator import InsightsGenerator  # noqa: E402


def test_insights_generator_returns_row_count(tmp_path):
    logger = Mock()
    file_adapter = Mock(spec=FileAdapter)
    generator = InsightsGenerator(file_adapter, logger)

    report_key = "open_sales_orders"
    headers = ["TxnID", "RefNumber"]
    rows = [["1", "SO001"], ["2", "SO002"]]

    insights = generator.generate_insights(
        report_key,
        headers,
        rows,
    )

    assert insights["row_count"] == 2
    assert insights["column_count"] == 2
    assert "generated_at" in insights


def test_insights_generator_writes_output_file(tmp_path):
    logger = Mock()
    file_adapter = Mock(spec=FileAdapter)
    generator = InsightsGenerator(file_adapter, logger)

    report_key = "open_sales_orders"
    headers = ["TxnID"]
    rows = [["1"]]
    output_path = tmp_path / "insights.json"

    generator.generate_insights(
        report_key,
        headers,
        rows,
        str(output_path),
    )

    file_adapter.write_file.assert_called_once()
    args, kwargs = file_adapter.write_file.call_args
    assert args[0] == str(output_path)
    assert "row_count" in args[1]