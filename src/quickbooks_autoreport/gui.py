"""GUI interface for QuickBooks Auto Reporter.

Provides a modern Tkinter-based interface with real-time status updates,
configuration management, and scheduling capabilities.
"""

import datetime as dt
import os
import subprocess
import sys
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from typing import Optional, Dict, Any

from . import (
    REPORT_CONFIGS,
    DEFAULT_OUT_DIR,
    load_settings,
    save_settings,
    export_all_reports,
)
from .services.scheduler import SchedulerManager
from .utils.logging_utils import log_info, log_error, log_success


class QuickBooksAutoReporterGUI:
    """Main GUI application class."""
    
    def __init__(self):
        """Initialize the GUI application."""
        self.root = tk.Tk()
        self.root.title("QuickBooks Autoreporter")
        self.root.geometry("900x700")
        self.root.resizable(False, False)
        
        # Load settings
        self.settings = load_settings()
        self.output_dir = self.settings["output_dir"]
        self.selected_interval = self.settings["interval"]
        
        # State variables
        self.scheduler_manager = SchedulerManager()
        self.last_export_time = None
        self.last_export_results = {}
        
        # Create GUI variables
        self.status_var = tk.StringVar(value="Idle")
        self.next_var = tk.StringVar(value="-")
        self.folder_var = tk.StringVar(value=self.output_dir)
        self.interval_var = tk.StringVar(value=self.selected_interval)
        self.last_check_var = tk.StringVar(value="-")
        self.time_since_var = tk.StringVar(value="-")
        self.date_from_var = tk.StringVar(value=self.settings["report_date_from"])
        self.date_to_var = tk.StringVar(value=self.settings["report_date_to"])
        
        # Report status variables
        self.report_status_vars = {}
        for report_key in REPORT_CONFIGS.keys():
            self.report_status_vars[report_key] = {
                "status": tk.StringVar(value="-"),
                "rows": tk.StringVar(value="-"),
                "excel": tk.StringVar(value="-"),
            }
        
        # Set up scheduler callbacks
        self.scheduler_manager.set_callbacks(
            status_callback=self.on_scheduler_status,
            error_callback=self.on_scheduler_error
        )
        
        self.create_widgets()
        self.start_timer_display()
        
        # Save settings on close
        self.root.protocol("WM_DELETE_WINDOW", self.on_exit)
    
    def create_widgets(self) -> None:
        """Create all GUI widgets."""
        # Title
        title_frame = tk.Frame(self.root)
        title_frame.pack(pady=(10, 5))
        tk.Label(
            title_frame, text="QuickBooks Autoreporter", font=("Segoe UI", 14, "bold")
        ).pack()
        tk.Label(
            title_frame,
            text=(
                "Automated exports • Change detection + snapshots • Styled Excel • "
                "Scheduled checks with folder selection"
            ),
            font=("Segoe UI", 10),
            fg="#666",
            wraplength=740,
            justify="center",
        ).pack()
        
        # Configuration section
        config_frame = tk.LabelFrame(
            self.root, text="Configuration", font=("Segoe UI", 10, "bold")
        )
        config_frame.pack(fill="x", padx=10, pady=5)
        
        # Output folder selection
        folder_frame = tk.Frame(config_frame)
        folder_frame.pack(fill="x", padx=10, pady=5)
        tk.Label(folder_frame, text="Output Folder:", width=15, anchor="w").pack(
            side="left"
        )
        tk.Entry(
            folder_frame, textvariable=self.folder_var, state="readonly", width=50
        ).pack(side="left", padx=5)
        tk.Button(
            folder_frame, text="Browse...", command=self.select_folder, width=10
        ).pack(side="right")
        
        # Interval selection
        interval_frame = tk.Frame(config_frame)
        interval_frame.pack(fill="x", padx=10, pady=5)
        tk.Label(interval_frame, text="Check Interval:", width=15, anchor="w").pack(
            side="left"
        )
        interval_combo = ttk.Combobox(
            interval_frame,
            textvariable=self.interval_var,
            values=list(["5 minutes", "15 minutes", "30 minutes", "60 minutes"]),
            state="readonly",
            width=15,
        )
        interval_combo.pack(side="left", padx=5)
        interval_combo.bind("<<ComboboxSelected>>", self.on_interval_changed)
        
        # Date range selection
        date_frame = tk.LabelFrame(
            config_frame,
            text="Date Range (for P&L, Sales, AP/AR Aging Reports)",
            font=("Segoe UI", 9, "bold"),
        )
        date_frame.pack(fill="x", padx=10, pady=5)
        
        # From date
        from_date_frame = tk.Frame(date_frame)
        from_date_frame.pack(fill="x", padx=10, pady=2)
        tk.Label(from_date_frame, text="From Date:", width=12, anchor="w").pack(
            side="left"
        )
        from_date_entry = tk.Entry(
            from_date_frame, textvariable=self.date_from_var, width=12
        )
        from_date_entry.pack(side="left", padx=5)
        from_date_entry.bind("<FocusOut>", self.on_date_changed)
        tk.Label(
            from_date_frame, text="(YYYY-MM-DD)", font=("Segoe UI", 8), fg="#666"
        ).pack(side="left", padx=5)
        
        # To date
        to_date_frame = tk.Frame(date_frame)
        to_date_frame.pack(fill="x", padx=10, pady=2)
        tk.Label(to_date_frame, text="To Date:", width=12, anchor="w").pack(side="left")
        to_date_entry = tk.Entry(to_date_frame, textvariable=self.date_to_var, width=12)
        to_date_entry.pack(side="left", padx=5)
        to_date_entry.bind("<FocusOut>", self.on_date_changed)
        tk.Label(
            to_date_frame, text="(YYYY-MM-DD)", font=("Segoe UI", 8), fg="#666"
        ).pack(side="left", padx=5)
        
        # Quick date buttons
        quick_date_frame = tk.Frame(date_frame)
        quick_date_frame.pack(fill="x", padx=10, pady=5)
        tk.Button(
            quick_date_frame,
            text="This Month",
            command=self.set_this_month,
            bg="#9C27B0",
            fg="white",
            font=("Segoe UI", 8),
            width=10,
        ).pack(side="left", padx=2)
        tk.Button(
            quick_date_frame,
            text="Last Month",
            command=self.set_last_month,
            bg="#9C27B0",
            fg="white",
            font=("Segoe UI", 8),
            width=10,
        ).pack(side="left", padx=2)
        tk.Button(
            quick_date_frame,
            text="This Year",
            command=self.set_this_year,
            bg="#9C27B0",
            fg="white",
            font=("Segoe UI", 8),
            width=10,
        ).pack(side="left", padx=2)
        tk.Button(
            quick_date_frame,
            text="Last Year",
            command=self.set_last_year,
            bg="#9C27B0",
            fg="white",
            font=("Segoe UI", 8),
            width=10,
        ).pack(side="left", padx=2)
        
        # Control buttons
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10)
        self.start_button = tk.Button(
            control_frame,
            text="Start Auto",
            width=12,
            command=self.start_scheduler,
            bg="#4CAF50",
            fg="white",
            font=("Segoe UI", 10, "bold"),
        )
        self.start_button.grid(row=0, column=0, padx=5)
        
        self.stop_button = tk.Button(
            control_frame,
            text="Stop",
            width=12,
            command=self.stop_scheduler,
            bg="#f44336",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            state="disabled",
        )
        self.stop_button.grid(row=0, column=1, padx=5)
        
        tk.Button(
            control_frame,
            text="Export All Now",
            width=15,
            command=self.export_now,
            bg="#2196F3",
            fg="white",
            font=("Segoe UI", 10, "bold"),
        ).grid(row=0, column=2, padx=5)
        tk.Button(
            control_frame,
            text="Open Folder",
            width=12,
            command=self.open_folder,
            bg="#FF9800",
            fg="white",
            font=("Segoe UI", 10, "bold"),
        ).grid(row=0, column=3, padx=5)
        
        # Status section
        status_frame = tk.LabelFrame(self.root, text="Status", font=("Segoe UI", 10, "bold"))
        status_frame.pack(fill="x", padx=10, pady=5)
        
        status_grid = tk.Frame(status_frame)
        status_grid.pack(padx=10, pady=5)
        
        # Status info
        tk.Label(status_grid, text="Status:", width=15, anchor="e").grid(
            row=0, column=0, sticky="e", padx=5, pady=2
        )
        tk.Label(
            status_grid,
            textvariable=self.status_var,
            fg="#006400",
            width=20,
            anchor="w",
        ).grid(row=0, column=1, sticky="w", padx=5, pady=2)
        tk.Label(status_grid, text="Next Run:", width=15, anchor="e").grid(
            row=0, column=2, sticky="e", padx=5, pady=2
        )
        tk.Label(status_grid, textvariable=self.next_var, width=25, anchor="w").grid(
            row=0, column=3, sticky="w", padx=5, pady=2
        )
        
        # Reports status
        reports_frame = tk.LabelFrame(
            self.root, text="Report Status", font=("Segoe UI", 10, "bold")
        )
        reports_frame.pack(fill="x", padx=10, pady=5)
        
        reports_grid = tk.Frame(reports_frame)
        reports_grid.pack(padx=10, pady=5)
        
        # Headers
        tk.Label(
            reports_grid, text="Report", font=("Segoe UI", 9, "bold"), width=20
        ).grid(row=0, column=0, padx=5, pady=2)
        tk.Label(
            reports_grid, text="Status", font=("Segoe UI", 9, "bold"), width=15
        ).grid(row=0, column=1, padx=5, pady=2)
        tk.Label(
            reports_grid, text="Rows", font=("Segoe UI", 9, "bold"), width=10
        ).grid(row=0, column=2, padx=5, pady=2)
        tk.Label(
            reports_grid, text="Excel", font=("Segoe UI", 9, "bold"), width=10
        ).grid(row=0, column=3, padx=5, pady=2)
        
        # Report rows
        for i, (report_key, config) in enumerate(REPORT_CONFIGS.items(), 1):
            tk.Label(reports_grid, text=config["name"], width=20, anchor="w").grid(
                row=i, column=0, padx=5, pady=2, sticky="w"
            )
            tk.Label(
                reports_grid,
                textvariable=self.report_status_vars[report_key]["status"],
                width=15,
                anchor="w",
            ).grid(row=i, column=1, padx=5, pady=2, sticky="w")
            tk.Label(
                reports_grid,
                textvariable=self.report_status_vars[report_key]["rows"],
                width=10,
                anchor="w",
            ).grid(row=i, column=2, padx=5, pady=2, sticky="w")
            tk.Label(
                reports_grid,
                textvariable=self.report_status_vars[report_key]["excel"],
                width=10,
                anchor="w",
            ).grid(row=i, column=3, padx=5, pady=2, sticky="w")
        
        # Exit button
        tk.Button(
            self.root,
            text="Exit",
            width=15,
            command=self.on_exit,
            bg="#795548",
            fg="white",
            font=("Segoe UI", 10, "bold"),
        ).pack(pady=(10, 10))
    
    def select_folder(self) -> None:
        """Open folder selection dialog."""
        folder = filedialog.askdirectory(
            title="Select Output Folder", initialdir=self.output_dir
        )
        if folder:
            self.output_dir = folder
            self.folder_var.set(folder)
            self.settings["output_dir"] = folder
            save_settings(self.settings)
    
    def on_interval_changed(self, event=None) -> None:
        """Handle interval selection change."""
        self.selected_interval = self.interval_var.get()
        self.settings["interval"] = self.selected_interval
        save_settings(self.settings)
        
        # Update scheduler if running
        if self.scheduler_manager.is_running():
            self.scheduler_manager.update_interval(self.selected_interval)
    
    def on_date_changed(self, event=None) -> None:
        """Handle date field changes."""
        try:
            # Validate date format
            from_date = self.date_from_var.get().strip()
            to_date = self.date_to_var.get().strip()
            
            if from_date:
                dt.datetime.strptime(from_date, "%Y-%m-%d")
                self.settings["report_date_from"] = from_date
            
            if to_date:
                dt.datetime.strptime(to_date, "%Y-%m-%d")
                self.settings["report_date_to"] = to_date
            
            save_settings(self.settings)
            
            # Update scheduler if running
            if self.scheduler_manager.is_running():
                self.scheduler_manager.update_date_range(
                    self.date_from_var.get().strip() or None,
                    self.date_to_var.get().strip() or None
                )
        except ValueError:
            pass  # Invalid date format - could show a warning
    
    def set_this_month(self) -> None:
        """Set date range to current month."""
        today = dt.date.today()
        first_day = today.replace(day=1)
        self.date_from_var.set(first_day.strftime("%Y-%m-%d"))
        self.date_to_var.set(today.strftime("%Y-%m-%d"))
        self.on_date_changed()
    
    def set_last_month(self) -> None:
        """Set date range to last month."""
        today = dt.date.today()
        first_day_this_month = today.replace(day=1)
        last_day_last_month = first_day_this_month - dt.timedelta(days=1)
        first_day_last_month = last_day_last_month.replace(day=1)
        self.date_from_var.set(first_day_last_month.strftime("%Y-%m-%d"))
        self.date_to_var.set(last_day_last_month.strftime("%Y-%m-%d"))
        self.on_date_changed()
    
    def set_this_year(self) -> None:
        """Set date range to current year."""
        today = dt.date.today()
        first_day_year = today.replace(month=1, day=1)
        self.date_from_var.set(first_day_year.strftime("%Y-%m-%d"))
        self.date_to_var.set(today.strftime("%Y-%m-%d"))
        self.on_date_changed()
    
    def set_last_year(self) -> None:
        """Set date range to last year."""
        today = dt.date.today()
        last_year = today.year - 1
        first_day_last_year = dt.date(last_year, 1, 1)
        last_day_last_year = dt.date(last_year, 12, 31)
        self.date_from_var.set(first_day_last_year.strftime("%Y-%m-%d"))
        self.date_to_var.set(last_day_last_year.strftime("%Y-%m-%d"))
        self.on_date_changed()
    
    def start_timer_display(self) -> None:
        """Start the timer display update loop."""
        self.update_timer_display()
        self.root.after(1000, self.start_timer_display)
    
    def update_timer_display(self) -> None:
        """Update the timer display."""
        if self.last_export_time:
            time_diff = dt.datetime.now() - self.last_export_time
            hours, remainder = divmod(int(time_diff.total_seconds()), 3600)
            minutes, seconds = divmod(remainder, 60)
            
            if hours > 0:
                time_str = f"{hours}h {minutes}m {seconds}s"
            elif minutes > 0:
                time_str = f"{minutes}m {seconds}s"
            else:
                time_str = f"{seconds}s"
            
            self.time_since_var.set(time_str)
        else:
            self.time_since_var.set("-")
        
        # Update next run time if scheduler is running
        if self.scheduler_manager.is_running():
            status = self.scheduler_manager.get_status()
            if status and status.get("time_until_next_run"):
                self.next_var.set(status["time_until_next_run"])
    
    def open_folder(self) -> None:
        """Open output folder in explorer."""
        os.makedirs(self.output_dir, exist_ok=True)
        if sys.platform == "win32":
            os.startfile(self.output_dir)
        elif sys.platform == "darwin":
            subprocess.run(["open", self.output_dir])
        else:
            subprocess.run(["xdg-open", self.output_dir])
    
    def start_scheduler(self) -> None:
        """Start scheduled exports."""
        if self.scheduler_manager.start(
            self.selected_interval,
            self.output_dir,
            self.date_from_var.get().strip() or None,
            self.date_to_var.get().strip() or None
        ):
            self.status_var.set("Running")
            self.start_button.config(state="disabled")
            self.stop_button.config(state="normal")
            log_info("Started scheduled exports", self.output_dir)
    
    def stop_scheduler(self) -> None:
        """Stop scheduled exports."""
        if self.scheduler_manager.stop():
            self.status_var.set("Stopped")
            self.next_var.set("-")
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")
            log_info("Stopped scheduled exports", self.output_dir)
    
    def export_now(self) -> None:
        """Trigger immediate export."""
        self.status_var.set("Exporting...")
        
        # Reset all report statuses
        for report_key in REPORT_CONFIGS.keys():
            self.report_status_vars[report_key]["status"].set("Working...")
            self.report_status_vars[report_key]["rows"].set("-")
            self.report_status_vars[report_key]["excel"].set("-")
        
        # Run export in background thread
        threading.Thread(
            target=self._export_worker,
            daemon=True
        ).start()
    
    def _export_worker(self) -> None:
        """Background export worker."""
        try:
            date_from = self.date_from_var.get().strip() or None
            date_to = self.date_to_var.get().strip() or None
            
            results, errors = export_all_reports(
                self.output_dir, date_from, date_to, self.on_report_status
            )
            
            # Update UI from main thread
            self.root.after(0, self._on_export_complete, results, errors)
            
        except Exception as e:
            self.root.after(0, self._on_export_error, str(e))
    
    def on_report_status(self, report_key: str, status: str, details: str) -> None:
        """Handle report status updates."""
        if report_key in self.report_status_vars:
            self.report_status_vars[report_key]["status"].set(status)
            if status in ["Success", "Partial"]:
                self.report_status_vars[report_key]["rows"].set(details)
                self.report_status_vars[report_key]["excel"].set("✅")
            elif status == "Error":
                self.report_status_vars[report_key]["rows"].set("-")
                self.report_status_vars[report_key]["excel"].set("❌")
    
    def on_scheduler_status(self, component: str, status: str, message: str) -> None:
        """Handle scheduler status updates."""
        if component == "scheduler":
            self.status_var.set(status)
    
    def on_scheduler_error(self, component: str, error: Exception) -> None:
        """Handle scheduler errors."""
        log_error(f"Scheduler error: {error}", self.output_dir)
    
    def _on_export_complete(self, results: Dict[str, Any], errors: Dict[str, str]) -> None:
        """Handle export completion."""
        self.last_export_time = dt.datetime.now()
        self.last_export_results = results
        
        # Update overall status
        if errors:
            self.status_var.set(f"Completed with {len(errors)} error(s)")
        else:
            self.status_var.set("All reports completed")
    
    def _on_export_error(self, msg: str) -> None:
        """Handle export error."""
        self.status_var.set("Error")
        messagebox.showerror("QuickBooks Autoreporter", msg)
    
    def on_exit(self) -> None:
        """Handle application exit."""
        self.stop_scheduler()
        save_settings(self.settings)
        self.root.destroy()
    
    def run(self) -> None:
        """Start the GUI main loop."""
        self.root.mainloop()


def run_gui() -> None:
    """Run the GUI application."""
    try:
        os.makedirs(DEFAULT_OUT_DIR, exist_ok=True)
        app = QuickBooksAutoReporterGUI()
        app.run()
    except Exception as e:
        print(f"GUI Error: {e}")
        log_error(f"GUI Fatal: {e}")
        raise


if __name__ == "__main__":
    run_gui()