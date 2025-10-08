"""Scheduling and polling engine for QuickBooks Auto Reporter.

Provides continuous polling functionality with configurable intervals
and graceful shutdown capabilities.
"""

import datetime as dt
import threading
import time
from typing import Callable, Optional

from ..config import INTERVAL_OPTIONS
from ..services.report_service import export_all_reports
from ..utils.logging_utils import log_info, log_error, log_progress, log_success


class SchedulerThread(threading.Thread):
    """Thread-based scheduler for continuous report polling."""
    
    def __init__(
        self,
        interval: str,
        out_dir: str,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        status_callback: Optional[Callable] = None,
        error_callback: Optional[Callable] = None
    ):
        """Initialize scheduler thread.
        
        Args:
            interval: Interval key from INTERVAL_OPTIONS
            out_dir: Output directory for reports
            date_from: Start date for reports with date ranges
            date_to: End date for reports with date ranges
            status_callback: Optional callback for status updates
            error_callback: Optional callback for error handling
        """
        super().__init__(daemon=True)
        self.interval_key = interval
        self.interval_seconds = INTERVAL_OPTIONS.get(interval, 15 * 60)  # Default to 15 minutes
        self.out_dir = out_dir
        self.date_from = date_from
        self.date_to = date_to
        self.status_callback = status_callback
        self.error_callback = error_callback
        
        self._stop_event = threading.Event()
        self._running = False
        self._last_run_time = None
        self._next_run_time = None
        self._run_count = 0
        self._error_count = 0
        
    def run(self) -> None:
        """Main scheduler loop."""
        self._running = True
        log_info(f"Scheduler started with {self.interval_key} interval", self.out_dir)
        
        if self.status_callback:
            self.status_callback("scheduler", "running", f"Polling every {self.interval_key}")
        
        while not self._stop_event.is_set():
            try:
                # Calculate next run time
                self._next_run_time = dt.datetime.now() + dt.timedelta(seconds=self.interval_seconds)
                
                # Execute report generation
                log_progress(f"Running scheduled export #{self._run_count + 1}", self.out_dir)
                
                if self.status_callback:
                    self.status_callback("scheduler", "running", f"Running export #{self._run_count + 1}")
                
                results, errors = export_all_reports(
                    self.out_dir,
                    self.date_from,
                    self.date_to,
                    self.status_callback
                )
                
                self._run_count += 1
                self._last_run_time = dt.datetime.now()
                
                # Log results
                successful_reports = len(results)
                failed_reports = len(errors)
                
                if failed_reports == 0:
                    log_success(
                        f"Scheduled export #{self._run_count} completed: "
                        f"{successful_reports} reports successful",
                        self.out_dir
                    )
                else:
                    log_error(
                        f"Scheduled export #{self._run_count} completed with errors: "
                        f"{successful_reports} successful, {failed_reports} failed",
                        self.out_dir
                    )
                    self._error_count += 1
                
                if self.status_callback:
                    if failed_reports == 0:
                        self.status_callback("scheduler", "success", f"Export #{self._run_count} completed")
                    else:
                        self.status_callback("scheduler", "partial", f"Export #{self._run_count} had errors")
                
                # Wait for next interval or stop signal
                if self._stop_event.wait(self.interval_seconds):
                    break
                    
            except Exception as e:
                self._error_count += 1
                log_error(f"Scheduler error: {e}", self.out_dir)
                
                if self.error_callback:
                    self.error_callback("scheduler", e)
                
                # Wait a shorter time before retrying after error
                if self._stop_event.wait(60):  # Wait 1 minute after error
                    break
        
        self._running = False
        log_info(f"Scheduler stopped after {self._run_count} runs", self.out_dir)
        
        if self.status_callback:
            self.status_callback("scheduler", "stopped", f"Completed {self._run_count} runs")
    
    def stop(self) -> None:
        """Stop the scheduler gracefully."""
        log_info("Stopping scheduler...", self.out_dir)
        self._stop_event.set()
    
    def is_running(self) -> bool:
        """Check if scheduler is currently running.
        
        Returns:
            True if running, False otherwise
        """
        return self._running
    
    def get_status(self) -> dict:
        """Get current scheduler status.
        
        Returns:
            Dictionary with status information
        """
        return {
            "running": self._running,
            "interval_key": self.interval_key,
            "interval_seconds": self.interval_seconds,
            "last_run_time": self._last_run_time.isoformat() if self._last_run_time else None,
            "next_run_time": self._next_run_time.isoformat() if self._next_run_time else None,
            "run_count": self._run_count,
            "error_count": self._error_count,
            "time_until_next_run": self._get_time_until_next_run()
        }
    
    def _get_time_until_next_run(self) -> Optional[str]:
        """Get time until next run in human-readable format.
        
        Returns:
            Human-readable time until next run or None if not scheduled
        """
        if not self._next_run_time:
            return None
        
        now = dt.datetime.now()
        if self._next_run_time <= now:
            return "Due now"
        
        delta = self._next_run_time - now
        total_seconds = int(delta.total_seconds())
        
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        if hours > 0:
            return f"{hours}h {minutes}m {seconds}s"
        elif minutes > 0:
            return f"{minutes}m {seconds}s"
        else:
            return f"{seconds}s"
    
    def update_interval(self, new_interval: str) -> None:
        """Update the polling interval.
        
        Args:
            new_interval: New interval key from INTERVAL_OPTIONS
        """
        if new_interval not in INTERVAL_OPTIONS:
            raise ValueError(f"Invalid interval: {new_interval}")
        
        old_interval = self.interval_key
        self.interval_key = new_interval
        self.interval_seconds = INTERVAL_OPTIONS[new_interval]
        
        log_info(f"Scheduler interval updated from {old_interval} to {new_interval}", self.out_dir)
        
        if self.status_callback:
            self.status_callback("scheduler", "running", f"Interval updated to {new_interval}")
    
    def update_date_range(self, date_from: Optional[str], date_to: Optional[str]) -> None:
        """Update the date range for reports.
        
        Args:
            date_from: Start date for reports with date ranges
            date_to: End date for reports with date ranges
        """
        self.date_from = date_from
        self.date_to = date_to
        
        log_info(f"Scheduler date range updated: {date_from} to {date_to}", self.out_dir)


class SchedulerManager:
    """Manager class for handling scheduler lifecycle."""
    
    def __init__(self):
        """Initialize scheduler manager."""
        self._scheduler: Optional[SchedulerThread] = None
        self._status_callback: Optional[Callable] = None
        self._error_callback: Optional[Callable] = None
    
    def set_callbacks(self, status_callback: Callable = None, error_callback: Callable = None) -> None:
        """Set callback functions for status and error updates.
        
        Args:
            status_callback: Callback for status updates
            error_callback: Callback for error handling
        """
        self._status_callback = status_callback
        self._error_callback = error_callback
    
    def start(
        self,
        interval: str,
        out_dir: str,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None
    ) -> bool:
        """Start the scheduler.
        
        Args:
            interval: Interval key from INTERVAL_OPTIONS
            out_dir: Output directory for reports
            date_from: Start date for reports with date ranges
            date_to: End date for reports with date ranges
            
        Returns:
            True if started successfully, False if already running
        """
        if self._scheduler and self._scheduler.is_running():
            return False
        
        self._scheduler = SchedulerThread(
            interval=interval,
            out_dir=out_dir,
            date_from=date_from,
            date_to=date_to,
            status_callback=self._status_callback,
            error_callback=self._error_callback
        )
        
        self._scheduler.start()
        return True
    
    def stop(self) -> bool:
        """Stop the scheduler.
        
        Returns:
            True if stopped successfully, False if not running
        """
        if not self._scheduler or not self._scheduler.is_running():
            return False
        
        self._scheduler.stop()
        self._scheduler.join(timeout=30)  # Wait up to 30 seconds for graceful shutdown
        
        return True
    
    def is_running(self) -> bool:
        """Check if scheduler is currently running.
        
        Returns:
            True if running, False otherwise
        """
        return self._scheduler is not None and self._scheduler.is_running()
    
    def get_status(self) -> Optional[dict]:
        """Get current scheduler status.
        
        Returns:
            Dictionary with status information or None if no scheduler
        """
        if not self._scheduler:
            return None
        
        return self._scheduler.get_status()
    
    def update_interval(self, new_interval: str) -> bool:
        """Update the polling interval.
        
        Args:
            new_interval: New interval key from INTERVAL_OPTIONS
            
        Returns:
            True if updated successfully, False if not running
        """
        if not self._scheduler or not self._scheduler.is_running():
            return False
        
        self._scheduler.update_interval(new_interval)
        return True
    
    def update_date_range(self, date_from: Optional[str], date_to: Optional[str]) -> bool:
        """Update the date range for reports.
        
        Args:
            date_from: Start date for reports with date ranges
            date_to: End date for reports with date ranges
            
        Returns:
            True if updated successfully, False if not running
        """
        if not self._scheduler or not self._scheduler.is_running():
            return False
        
        self._scheduler.update_date_range(date_from, date_to)
        return True