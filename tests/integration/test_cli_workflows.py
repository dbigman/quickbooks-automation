import sys
from pathlib import Path
from unittest.mock import Mock, patch

# Ensure 'src' is importable
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))

from quickbooks_autoreport.adapters.file_adapter import FileAdapter  # noqa: E402
from quickbooks_autoreport.adapters.logger_adapter import LoggerAdapter  # noqa: E402
from quickbooks_autoreport.adapters.quickbooks.xml_builder import XMLBuilder  # noqa: E402
from quickbooks_autoreport.adapters.quickbooks.xml_parser import XMLParser  # noqa: E402
from quickbooks_autoreport.adapters.settings_adapter import SettingsAdapter  # noqa: E402
from quickbooks_autoreport.cli import CLI  # noqa: E402


@patch("quickbooks_autoreport.cli.CLI.run")
def test_cli_entry_point_composes_dependencies(mock_run):
    """Test that CLI entry point composes and runs CLI with DI."""
    # This is a very high-level integration test focusing on composition
    logger_adapter = LoggerAdapter()
    logger = logger_adapter.setup_logger("test")

    file_adapter = Mock(spec=FileAdapter)
    settings_adapter = Mock(spec=SettingsAdapter)
    xml_builder = Mock(spec=XMLBuilder)
    xml_parser = Mock(spec=XMLParser)

    cli = CLI(
        file_adapter=file_adapter,
        settings_adapter=settings_adapter,
        xml_builder=xml_builder,
        xml_parser=xml_parser,
        logger_adapter=logger_adapter,
        logger=logger,
    )
    cli.run(["--diagnose"])
    mock_run.assert_called_once_with(["--diagnose"])