"""CLI entry point for QuickBooks Auto Reporter.

Composes services with dependency injection and delegates to CLI logic.
"""

import logging
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))

from quickbooks_autoreport.adapters.file_adapter import FileAdapter  # noqa: E402
from quickbooks_autoreport.adapters.logger_adapter import LoggerAdapter  # noqa: E402
from quickbooks_autoreport.adapters.quickbooks.xml_builder import XMLBuilder  # noqa: E402
from quickbooks_autoreport.adapters.quickbooks.xml_parser import XMLParser  # noqa: E402
from quickbooks_autoreport.adapters.settings_adapter import SettingsAdapter  # noqa: E402
from quickbooks_autoreport.cli import CLI  # noqa: E402
from quickbooks_autoreport.domain.settings import Settings  # noqa: E402


def main() -> None:
    """Entry point for CLI application."""
    # Setup logger
    logger_adapter = LoggerAdapter()
    logger = logger_adapter.setup_logger("qb_auto_reporter_cli")

    # Compose dependencies
    file_adapter = FileAdapter(logger)
    settings_adapter = SettingsAdapter(
        "~/.qb_auto_reporter_settings.json", logger
    )
    xml_builder = XMLBuilder()
    xml_parser = XMLParser()

    # Initialize CLI with dependencies
    cli = CLI(
        file_adapter=file_adapter,
        settings_adapter=settings_adapter,
        xml_builder=xml_builder,
        xml_parser=xml_parser,
        logger_adapter=logger_adapter,
        logger=logger,
    )

    # Run CLI
    try:
        cli.run(sys.argv[1:])
    except Exception as e:
        logger.exception("CLI failed: %s", e)
        sys.exit(1)


if __name__ == "__main__":
    main()