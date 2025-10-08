import sys
from pathlib import Path
from unittest.mock import Mock

# Ensure 'src' is importable
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))

from quickbooks_autoreport.adapters.file_adapter import FileAdapter  # noqa: E402
from quickbooks_autoreport.adapters.logger_adapter import LoggerAdapter  # noqa: E402
from quickbooks_autoreport.adapters.quickbooks.xml_builder import XMLBuilder  # noqa: E402
from quickbooks_autoreport.adapters.quickbooks.xml_parser import XMLParser  # noqa: E402
from quickbooks_autoreport.adapters.settings_adapter import SettingsAdapter  # noqa: E402
from quickbooks_autoreport.gui import GUI  # noqa: E402


def test_gui_initializes_with_dependencies():
    """Test that GUI can be initialized with all dependencies injected."""
    logger_adapter = LoggerAdapter()
    logger = logger_adapter.setup_logger("test")

    file_adapter = Mock(spec=FileAdapter)
    settings_adapter = Mock(spec=SettingsAdapter)
    xml_builder = Mock(spec=XMLBuilder)
    xml_parser = Mock(spec=XMLParser)

    gui = GUI(
        file_adapter=file_adapter,
        settings_adapter=settings_adapter,
        xml_builder=xml_builder,
        xml_parser=xml_parser,
        logger_adapter=logger_adapter,
        logger=logger,
    )

    # Verify GUI was instantiated (mocks prevent actual GUI launch)
    assert gui is not None
    assert gui._file_adapter is file_adapter
    assert gui._settings_adapter is settings_adapter
    assert gui._xml_builder is xml_builder
    assert gui._xml_parser is xml_parser
    assert gui._logger_adapter is logger_adapter
    assert gui._logger is logger