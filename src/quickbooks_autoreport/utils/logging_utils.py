"""Logging utilities for QuickBooks Auto Reporter."""

import datetime as dt
import os
import threading
from typing import Optional

from ..config import DEFAULT_OUT_DIR


# Thread-safe logging
_log_lock = threading.Lock()


def log(msg: str, out_dir: Optional[str] = None) -> None:
    """Log message to file with timestamp and emoji indicators.
    
    Args:
        msg: Message to log
        out_dir: Output directory (uses default if None)
    """
    if out_dir is None:
        out_dir = DEFAULT_OUT_DIR
    
    ts = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Ensure directory exists
    try:
        os.makedirs(out_dir, exist_ok=True)
    except Exception:
        return
    
    log_file = os.path.join(out_dir, "QuickBooks_Auto_Reports.log")
    
    # Thread-safe file writing
    with _log_lock:
        try:
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(f"[{ts}] {msg}\n")
        except Exception:
            pass


def log_with_emoji(msg: str, emoji: str, out_dir: Optional[str] = None) -> None:
    """Log message with emoji indicator.
    
    Args:
        msg: Message to log
        emoji: Emoji indicator (📥 📊 🎯 ✅ ❌)
        out_dir: Output directory (uses default if None)
    """
    log(f"{emoji} {msg}", out_dir)


def log_info(msg: str, out_dir: Optional[str] = None) -> None:
    """Log info message.
    
    Args:
        msg: Message to log
        out_dir: Output directory (uses default if None)
    """
    log_with_emoji(msg, "📋", out_dir)


def log_success(msg: str, out_dir: Optional[str] = None) -> None:
    """Log success message.
    
    Args:
        msg: Message to log
        out_dir: Output directory (uses default if None)
    """
    log_with_emoji(msg, "✅", out_dir)


def log_error(msg: str, out_dir: Optional[str] = None) -> None:
    """Log error message.
    
    Args:
        msg: Message to log
        out_dir: Output directory (uses default if None)
    """
    log_with_emoji(msg, "❌", out_dir)


def log_warning(msg: str, out_dir: Optional[str] = None) -> None:
    """Log warning message.
    
    Args:
        msg: Message to log
        out_dir: Output directory (uses default if None)
    """
    log_with_emoji(msg, "⚠️", out_dir)


def log_progress(msg: str, out_dir: Optional[str] = None) -> None:
    """Log progress message.
    
    Args:
        msg: Message to log
        out_dir: Output directory (uses default if None)
    """
    log_with_emoji(msg, "🔄", out_dir)


def log_data(msg: str, out_dir: Optional[str] = None) -> None:
    """Log data-related message.
    
    Args:
        msg: Message to log
        out_dir: Output directory (uses default if None)
    """
    log_with_emoji(msg, "📊", out_dir)


def log_target(msg: str, out_dir: Optional[str] = None) -> None:
    """Log target/goal message.
    
    Args:
        msg: Message to log
        out_dir: Output directory (uses default if None)
    """
    log_with_emoji(msg, "🎯", out_dir)


def log_receive(msg: str, out_dir: Optional[str] = None) -> None:
    """Log data receive message.
    
    Args:
        msg: Message to log
        out_dir: Output directory (uses default if None)
    """
    log_with_emoji(msg, "📥", out_dir)


def log_diagnostic(msg: str, out_dir: Optional[str] = None) -> None:
    """Log diagnostic message.
    
    Args:
        msg: Message to log
        out_dir: Output directory (uses default if None)
    """
    log_with_emoji(msg, "🔍", out_dir)


def log_insight(msg: str, out_dir: Optional[str] = None) -> None:
    """Log insight message.
    
    Args:
        msg: Message to log
        out_dir: Output directory (uses default if None)
    """
    log_with_emoji(msg, "💡", out_dir)


def log_separator(out_dir: Optional[str] = None) -> None:
    """Log separator line.
    
    Args:
        out_dir: Output directory (uses default if None)
    """
    log("=" * 60, out_dir)