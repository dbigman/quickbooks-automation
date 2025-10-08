"""Shared utility functions for QuickBooks Auto Reporter."""

from .file_utils import (
    sha256_text,
    snapshot_filename,
    compute_data_hash,
    should_create_snapshot,
    save_hash,
    create_snapshot,
    ensure_directory_exists,
)

from .logging_utils import (
    log,
    log_with_emoji,
    log_info,
    log_success,
    log_error,
    log_warning,
    log_progress,
    log_data,
    log_target,
    log_receive,
    log_diagnostic,
    log_insight,
    log_separator,
)

__all__ = [
    # File utilities
    "sha256_text",
    "snapshot_filename",
    "compute_data_hash",
    "should_create_snapshot",
    "save_hash",
    "create_snapshot",
    "ensure_directory_exists",
    
    # Logging utilities
    "log",
    "log_with_emoji",
    "log_info",
    "log_success",
    "log_error",
    "log_warning",
    "log_progress",
    "log_data",
    "log_target",
    "log_receive",
    "log_diagnostic",
    "log_insight",
    "log_separator",
]