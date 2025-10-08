"""File utility functions for QuickBooks Auto Reporter."""

import datetime as dt
import hashlib
import os
from typing import Dict, Any

from ..config import get_file_paths


def sha256_text(s: str) -> str:
    """Generate SHA-256 hash of text string.
    
    Args:
        s: Text string to hash
        
    Returns:
        SHA-256 hash as hexadecimal string
    """
    return hashlib.sha256(s.encode("utf-8", "ignore")).hexdigest()


def snapshot_filename(out_dir: str, report_key: str) -> str:
    """Generate timestamped snapshot filename.
    
    Args:
        out_dir: Output directory path
        report_key: Report configuration key
        
    Returns:
        Timestamped filename for snapshot
    """
    ts = dt.datetime.now().strftime("%Y-%m-%d_%H%M%S")
    main_csv = get_file_paths(out_dir, report_key)["main_csv"]
    base, ext = os.path.splitext(main_csv)
    return f"{base}_{ts}{ext}"


def compute_data_hash(csv_text: str) -> str:
    """Compute hash of CSV data for change detection.
    
    Args:
        csv_text: CSV content as string
        
    Returns:
        SHA-256 hash of the data
    """
    return sha256_text(csv_text)


def should_create_snapshot(out_dir: str, report_key: str, new_hash: str) -> bool:
    """Determine if snapshot should be created based on hash comparison.
    
    Args:
        out_dir: Output directory path
        report_key: Report configuration key
        new_hash: New hash to compare
        
    Returns:
        True if snapshot should be created (hash differs or file missing)
    """
    file_paths = get_file_paths(out_dir, report_key)
    hash_file = file_paths["hash_file"]
    
    if not os.path.exists(hash_file):
        return True
    
    try:
        with open(hash_file, "r", encoding="utf-8") as f:
            stored_hash = f.read().strip()
        return stored_hash != new_hash
    except Exception:
        return True


def save_hash(out_dir: str, report_key: str, hash_value: str) -> None:
    """Save hash value to file.
    
    Args:
        out_dir: Output directory path
        report_key: Report configuration key
        hash_value: Hash value to save
    """
    file_paths = get_file_paths(out_dir, report_key)
    hash_file = file_paths["hash_file"]
    
    try:
        with open(hash_file, "w", encoding="utf-8") as f:
            f.write(hash_value)
    except Exception:
        pass


def create_snapshot(out_dir: str, report_key: str, csv_content: str) -> str:
    """Create timestamped snapshot file.
    
    Args:
        out_dir: Output directory path
        report_key: Report configuration key
        csv_content: CSV content to save
        
    Returns:
        Path to created snapshot file
    """
    snapshot_path = snapshot_filename(out_dir, report_key)
    
    try:
        with open(snapshot_path, "w", newline="", encoding="utf-8") as f:
            f.write(csv_content)
        return snapshot_path
    except Exception:
        return ""


def ensure_directory_exists(path: str) -> None:
    """Ensure directory exists, create if it doesn't.
    
    Args:
        path: Directory path to ensure exists
    """
    try:
        os.makedirs(path, exist_ok=True)
    except Exception:
        pass