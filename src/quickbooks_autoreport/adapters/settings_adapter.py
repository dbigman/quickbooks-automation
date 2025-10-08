"""Settings persistence adapter for QuickBooks Auto Reporter.

Wraps configuration loading/saving with a clean interface.
"""

import json
import logging
import os
from pathlib import Path

from quickbooks_autoreport.domain.settings import Settings


class SettingsAdapter:
    """Manages settings persistence with dependency injection."""

    def __init__(self, settings_file: str, logger: logging.Logger) -> None:
        """Initialize with settings file path and injected logger."""
        self._settings_file = settings_file
        self._logger = logger

    def load_settings(self) -> Settings:
        """Load settings from file."""
        if not os.path.exists(self._settings_file):
            self._logger.info(
                f"Settings file not found: {self._settings_file}; using defaults"
            )
            return self.get_default_settings()

        try:
            with open(self._settings_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            settings = Settings(**data)
            settings.validate()
            self._logger.info(f"Loaded settings from {self._settings_file}")
            return settings
        except Exception as e:
            self._logger.error(f"Failed to load settings: {e}")
            raise

    def save_settings(self, settings: Settings) -> None:
        """Save settings to file."""
        settings.validate()
        try:
            # Ensure directory exists
            Path(self._settings_file).parent.mkdir(parents=True, exist_ok=True)
            with open(self._settings_file, "w", encoding="utf-8") as f:
                json.dump(settings.__dict__, f, indent=2, ensure_ascii=False)
            self._logger.info(f"Saved settings to {self._settings_file}")
        except Exception as e:
            self._logger.error(f"Failed to save settings: {e}")
            raise

    def get_default_settings(self) -> Settings:
        """Get default settings."""
        return Settings()