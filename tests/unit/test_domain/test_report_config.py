import sys
from pathlib import Path

# Ensure 'src' is importable
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))

from quickbooks_autoreport.domain.report_config import ReportConfig  # noqa: E402


def make_valid_config() -> ReportConfig:
    return ReportConfig(
        key="open_sales_orders",
        name="Open Sales Orders by Item",
        qbxml_type="OpenSalesOrderByItem",
        query_type="GeneralDetail",
        csv_filename="Open_Sales_Orders_By_Item.csv",
        excel_filename="Open_Sales_Orders_By_Item.xlsx",
        hash_filename="Open_Sales_Orders_By_Item.hash",
        request_log="open_so_request.xml",
        response_log="open_so_response.xml",
        uses_date_range=False,
    )


def test_get_file_paths_contains_expected_keys(tmp_path):
    cfg = make_valid_config()
    out_dir = str(tmp_path)

    paths = cfg.get_file_paths(out_dir)

    required_keys = [
        "main_csv",
        "excel_file",
        "hash_file",
        "log_file",
        "req_log",
        "resp_log",
    ]

    for k in required_keys:
        assert k in paths, f"Missing key in paths: {k}"

    # All paths should start with output dir
    for name, p in paths.items():
        assert isinstance(p, str), f"Path for {name} must be string"
        assert p.startswith(out_dir), (
            f"Path for {name} should start with output dir"
        )

    # Suffix checks for filenames
    assert paths["main_csv"].endswith(cfg.csv_filename)
    assert paths["excel_file"].endswith(cfg.excel_filename)
    assert paths["hash_file"].endswith(cfg.hash_filename)
    assert paths["req_log"].endswith(cfg.request_log)
    assert paths["resp_log"].endswith(cfg.response_log)
    assert paths["log_file"].endswith("QuickBooks_Auto_Reports.log")


def test_validate_success_does_not_raise():
    cfg = make_valid_config()
    # Should not raise
    cfg.validate()


def test_validate_invalid_query_type_raises():
    cfg = ReportConfig(
        key="k",
        name="Name",
        qbxml_type="SomeType",
        query_type="NotAValidType",
        csv_filename="a.csv",
        excel_filename="a.xlsx",
        hash_filename="a.hash",
        request_log="req.xml",
        response_log="resp.xml",
        uses_date_range=False,
    )
    raised = False
    try:
        cfg.validate()
    except ValueError as e:
        raised = True
        assert "Invalid query_type" in str(e)
    assert raised, "Expected ValueError for invalid query_type"


def test_validate_missing_required_fields_raise():
    # Empty key
    cfg = ReportConfig(
        key="",
        name="Name",
        qbxml_type="Type",
        query_type="GeneralDetail",
        csv_filename="a.csv",
        excel_filename="a.xlsx",
        hash_filename="a.hash",
        request_log="req.xml",
        response_log="resp.xml",
        uses_date_range=False,
    )
    try:
        cfg.validate()
        assert False, "Expected ValueError for empty key"
    except ValueError as e:
        assert "Report key cannot be empty" in str(e)

    # Empty name
    cfg = ReportConfig(
        key="k",
        name="",
        qbxml_type="Type",
        query_type="GeneralDetail",
        csv_filename="a.csv",
        excel_filename="a.xlsx",
        hash_filename="a.hash",
        request_log="req.xml",
        response_log="resp.xml",
        uses_date_range=False,
    )
    try:
        cfg.validate()
        assert False, "Expected ValueError for empty name"
    except ValueError as e:
        assert "Report name cannot be empty" in str(e)

    # Empty qbxml_type
    cfg = ReportConfig(
        key="k",
        name="Name",
        qbxml_type="",
        query_type="GeneralDetail",
        csv_filename="a.csv",
        excel_filename="a.xlsx",
        hash_filename="a.hash",
        request_log="req.xml",
        response_log="resp.xml",
        uses_date_range=False,
    )
    try:
        cfg.validate()
        assert False, "Expected ValueError for empty qbXML type"
    except ValueError as e:
        assert "qbXML type cannot be empty" in str(e)

    # Empty csv/excel filenames
    cfg = ReportConfig(
        key="k",
        name="Name",
        qbxml_type="Type",
        query_type="GeneralDetail",
        csv_filename="",
        excel_filename="a.xlsx",
        hash_filename="a.hash",
        request_log="req.xml",
        response_log="resp.xml",
        uses_date_range=False,
    )
    try:
        cfg.validate()
        assert False, "Expected ValueError for empty CSV filename"
    except ValueError as e:
        assert "CSV filename cannot be empty" in str(e)

    cfg = ReportConfig(
        key="k",
        name="Name",
        qbxml_type="Type",
        query_type="GeneralDetail",
        csv_filename="a.csv",
        excel_filename="",
        hash_filename="a.hash",
        request_log="req.xml",
        response_log="resp.xml",
        uses_date_range=False,
    )
    try:
        cfg.validate()
        assert False, "Expected ValueError for empty Excel filename"
    except ValueError as e:
        assert "Excel filename cannot be empty" in str(e)