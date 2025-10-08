import sys
from pathlib import Path
from unittest.mock import Mock, patch

# Ensure 'src' is importable
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))

from quickbooks_autoreport.adapters.quickbooks.request_handler import RequestHandler  # noqa: E402


def test_request_handler_sends_request():
    """Test that RequestHandler sends XML request to QuickBooks."""
    mock_session = Mock()
    handler = RequestHandler(mock_session)

    request_xml = "<QBXML>...</QBXML>"
    mock_response = Mock()
    mock_response.xml = "<QBXML>Response</QBXML>"
    mock_session.ProcessRequest.return_value = mock_response

    response = handler.send_request(request_xml)

    assert response == "<QBXML>Response</QBXML>"
    mock_session.ProcessRequest.assert_called_once_with(request_xml)


def test_request_handler_handles_error():
    """Test handling of request errors."""
    mock_session = Mock()
    handler = RequestHandler(mock_session)

    request_xml = "<QBXML>...</QBXML>"
    mock_session.ProcessRequest.side_effect = Exception("Request failed")

    try:
        handler.send_request(request_xml)
    except Exception as e:
        assert "Request failed" in str(e)