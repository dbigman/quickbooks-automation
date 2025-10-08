import sys
from pathlib import Path
from unittest.mock import Mock

# Ensure 'src' is importable
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))

from quickbooks_autoreport.adapters.file_adapter import FileAdapter  # noqa: E402
from quickbooks_autoreport.services.csv_creator import CSVCreator  # noqa: E402


def test_csv_creator_writes_file(tmp_path):
    logger = Mock()
    file_adapter = Mock(spec=FileAdapter)
    creator = CSVCreator(file_adapter, logger)

    path = tmp_path / "test.csv"
    headers = ["ID", "Name"]
    rows = [["1", "Alice"], ["2", "Bob"]]

    creator.create_csv(str(path), headers, rows)

    file_adapter.write_file.assert_called_once()
    args, kwargs = file_adapter.write_file.call_args
    assert args[0] == str(path)
    assert "ID,Name" in args[1]
    assert "1,Alice" in args[1]
    assert "2,Bob" in args[1]