import sys
from pathlib import Path

import pytest

# Ensure 'src' is importable
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))

from quickbooks_autoreport.adapters.file_adapter import FileAdapter  # noqa: E402


def test_file_adapter_hash_computation(tmp_path):
    logger = __import__("logging").getLogger("test")
    adapter = FileAdapter(logger)
    content = "test data"

    expected_hash = "a54d88e06612d82112c97f39d217f140a318c055d1144adec2544f3a47304c0f"
    assert adapter.compute_hash(content) == expected_hash


def test_file_adapter_write_read_file(tmp_path):
    logger = __import__("logging").getLogger("test")
    adapter = FileAdapter(logger)
    path = tmp_path / "test.txt"
    content = "hello world"

    adapter.write_file(str(path), content)
    assert adapter.file_exists(str(path))
    assert adapter.read_file(str(path)) == content


def test_file_adapter_ensure_directory(tmp_path):
    logger = __import__("logging").getLogger("test")
    adapter = FileAdapter(logger)
    dir_path = tmp_path / "subdir"
    adapter.ensure_directory(str(dir_path))
    assert dir_path.is_dir()


def test_file_adapter_read_write_hash(tmp_path):
    logger = __import__("logging").getLogger("test")
    adapter = FileAdapter(logger)
    hash_path = tmp_path / "test.hash"
    hash_value = "abcdef123456"

    adapter.write_hash(str(hash_path), hash_value)
    assert adapter.read_hash(str(hash_path)) == hash_value


def test_file_adapter_read_hash_missing_file(tmp_path):
    logger = __import__("logging").getLogger("test")
    adapter = FileAdapter(logger)
    assert adapter.read_hash(str(tmp_path / "missing.hash")) is None