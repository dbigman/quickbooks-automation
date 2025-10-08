import sys
from pathlib import Path
from unittest.mock import Mock

# Ensure 'src' is importable
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))

from quickbooks_autoreport.adapters.file_adapter import FileAdapter  # noqa: E402
from quickbooks_autoreport.services.excel_creator import ExcelCreator  # noqa: E402


def test_excel_creator_writes_mock_file(tmp_path):
    logger = Mock()
    file_adapter = Mock(spec=FileAdapter)
    creator = ExcelCreator(file_adapter, logger)

    path = tmp_path / "test.xlsx"
    headers = ["ID", "Name"]
    rows = [["1", "Alice"], ["2", "Bob"]]

    result = creator.create_excel(str(path), headers, rows)

    assert result is True
    file_adapter.write_file.assert_called_once()
    args, kwargs = file_adapter.write_file.call_args
    assert args[0] == str(path)
    assert "Mock Excel with" in args[1]