import sys
from pathlib import Path

# Ensure 'src' is importable
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))

from quickbooks_autoreport.adapters.quickbooks.error_handler import ErrorHandler  # noqa: E402


def test_error_handler_formats_com_error():
    """Test formatting of COM errors into user-friendly messages."""
    handler = ErrorHandler()

    com_error = Exception("COM error -2147221005: Invalid class string")
    error_info = handler.format_error(com_error)

    assert error_info["error_type"] == "SDK_NOT_INSTALLED"
    assert "Install QuickBooks SDK" in error_info["solutions"][0]


def test_error_handler_handles_generic_error():
    """Test handling of generic errors."""
    handler = ErrorHandler()

    generic_error = Exception("Some unknown error")
    error_info = handler.format_error(generic_error)

    assert error_info["error_type"] == "UNKNOWN_ERROR"
    assert len(error_info["solutions"]) > 0