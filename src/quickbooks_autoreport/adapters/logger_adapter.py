"""Logging adapter for QuickBooks Auto Reporter.

Wraps logging_utils to provide a clean interface for other adapters and services.
"""

import logging
from typing import Optional

from quickbooks_autoreport.utils.logging_utils import (  # noqa: E402
    setup_logger as setup_base_logger,
)


class LoggerAdapter:
    """Adapter for logging configuration and emoji-enhanced messages."""

    @staticmethod
    def setup_logger(
        name: str,
        log_file: Optional[str] = None,
        level: int = logging.INFO,
    ) -> logging.Logger:
        """Setup and return a configured logger.

        Args:
            name: Logger name
            log_file: Optional log file path
            level: Logging level

        Returns:
            Configured logger instance
        """
        return setup_base_logger(name, log_file, level)

    @staticmethod
    def log_with_emoji(
        logger: logging.Logger,
        level: int,
        emoji: str,
        message: str,
    ) -> None:
        """Log message with emoji prefix.

        Args:
            logger: Logger instance
            level: Logging level
            emoji: Emoji to prefix message
            message: Log message
        """
        from quickbooks_autoreport.utils.logging_utils import (  # noqa: E402
            log_with_emoji as base_log,
        )

        base_log(logger, level, emoji, message)