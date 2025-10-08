import json
import sys
from pathlib import Path

# Ensure 'src' is importable
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))

from quickbooks_autoreport.adapters.settings_adapter import SettingsAdapter  # noqa: E402
from quickbooks_autoreport.domain.settings import Settings


def test_settings_load_save_roundtrip(tmp_path):
    settings_file = tmp_path / "settings.json"
    logger = __import__("logging").getLogger("test")
    adapter = SettingsAdapter(str(settings_file), logger)
    original = Settings(output_dir=str(tmp_path), interval="30 minutes")
    adapter.save_settings(original)
    loaded = adapter.load_settings()
    assert loaded.output_dir == original.output_dir
    assert loaded.interval == original.interval


def test_settings_load_default_when_missing(tmp_path):
    settings_file = tmp_path / "missing.json"
    logger = __import__("logging").getLogger("test")
    adapter = SettingsAdapter(str(settings_file), logger)
    settings = adapter.load_settings()
    assert isinstance(settings, Settings)


def test_settings_save_creates_directory(tmp_path):
    settings_file = tmp_path / "subdir" / "settings.json"
    logger = __import__("logging").getLogger("test")
    adapter = SettingsAdapter(str(settings_file), logger)
    adapter.save_settings(Settings())
    assert settings_file.exists()