import sys
from pathlib import Path
from unittest.mock import Mock, patch

# Ensure 'src' is importable
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))

from quickbooks_autoreport.services.scheduler import Scheduler  # noqa: E402


def test_scheduler_start_stop():
    logger = Mock()
    scheduler = Scheduler(logger)

    scheduler.start()
    assert scheduler.is_running() is True

    scheduler.stop()
    assert scheduler.is_running() is False


@patch("threading.Thread")
def test_scheduler_schedules_task(mock_thread):
    logger = Mock()
    scheduler = Scheduler(logger)

    task = Mock()
    scheduler.start()
    scheduler.schedule_task(task, interval_seconds=60)

    # Verify thread was started
    mock_thread.assert_called()
    scheduler.stop()