import sys
from pathlib import Path
from unittest.mock import Mock, patch

# Ensure 'src' is importable
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))

from quickbooks_autoreport.adapters.quickbooks.connection import QuickBooksConnection  # noqa: E402


def test_connection_context_manager():
    """Test that QuickBooksConnection acts as a context manager."""
    with patch("quickbooks_autoreport.adapters.quickbooks.connection.client.Dispatch") as mock_dispatch:
        mock_instance = Mock()
        mock_dispatch.return_value = mock_instance

        # Mock the OpenConnection2 method
        mock_instance.OpenConnection2.return_value = "session_token"

        conn = QuickBooksConnection()
        with conn as session:
            assert session == "session_token"
            mock_instance.OpenConnection2.assert_called_once()

        # Verify CloseConnection was called on exit
        mock_instance.CloseConnection.assert_called_once()


def test_connection_failure():
    """Test handling of connection failures."""
    with patch("quickbooks_autoreport.adapters.quickbooks.connection.client.Dispatch") as mock_dispatch:
        mock_instance = Mock()
        mock_dispatch.return_value = mock_instance

        # Simulate connection error
        mock_instance.OpenConnection2.side_effect = Exception("COM error")

        conn = QuickBooksConnection()
        try:
            with conn:
                pass
        except Exception as e:
            assert "COM error" in str(e)