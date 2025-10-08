"""Command-line interface for QuickBooks Auto Reporter.

Provides comprehensive CLI functionality with multiple modes:
- GUI mode for interactive use
- CLI mode for automated operation
- Diagnostic mode for troubleshooting
- XML test mode for validation
"""

import argparse
import sys
from typing import Optional

from . import (
    __version__,
    DEFAULT_OUT_DIR,
    load_settings,
    save_settings,
    export_all_reports,
    diagnose_quickbooks_connection,
    test_xml_generation,
)
from .services.diagnostics_service import print_diagnostics_summary
from .utils.logging_utils import log_info, log_error, log_success, log_separator


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments.
    
    Returns:
        Parsed arguments namespace
    """
    parser = argparse.ArgumentParser(
        prog="quickbooks-autoreport",
        description="QuickBooks Auto Reporter - Automated report generation with change detection",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  quickbooks-autoreport --gui                    # Launch GUI interface
  quickbooks-autoreport --diagnose              # Run diagnostics
  quickbooks-autoreport --test-xml               # Test XML generation
  quickbooks-autoreport --output ./reports      # Export to custom directory
  quickbooks-autoreport --date-from 2025-01-01 --date-to 2025-01-31  # Custom date range
        """
    )
    
    # Mode selection
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument(
        "--gui",
        action="store_true",
        help="Launch GUI interface (default for executable)"
    )
    mode_group.add_argument(
        "--diagnose",
        action="store_true",
        help="Run QuickBooks connectivity diagnostics"
    )
    mode_group.add_argument(
        "--test-xml",
        action="store_true",
        help="Test XML generation for all report types"
    )
    
    # Output options
    parser.add_argument(
        "--output", "-o",
        default=DEFAULT_OUT_DIR,
        help=f"Output directory (default: {DEFAULT_OUT_DIR})"
    )
    
    # Date range options
    parser.add_argument(
        "--date-from",
        help="Start date for reports with date ranges (YYYY-MM-DD)"
    )
    parser.add_argument(
        "--date-to",
        help="End date for reports with date ranges (YYYY-MM-DD)"
    )
    
    # Configuration options
    parser.add_argument(
        "--interval",
        choices=["5 minutes", "15 minutes", "30 minutes", "60 minutes"],
        help="Set default polling interval (for GUI mode)"
    )
    
    # Other options
    parser.add_argument(
        "--version",
        action="version",
        version=f"QuickBooks Auto Reporter v{__version__}"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    
    return parser.parse_args()


def run_cli_mode(args: argparse.Namespace) -> int:
    """Run in command-line mode.
    
    Args:
        args: Parsed command-line arguments
        
    Returns:
        Exit code (0 for success, 1 for error)
    """
    print("QuickBooks Auto Reporter v{}".format(__version__))
    print("=" * 50)
    print("Available reports: Open Sales Orders, Profit & Loss, Sales by Item")
    print("")
    
    # Load settings for date range
    settings = load_settings()
    date_from = args.date_from or settings.get("report_date_from")
    date_to = args.date_to or settings.get("report_date_to")
    
    if args.verbose:
        print(f"Output directory: {args.output}")
        if date_from and date_to:
            print(f"Date range: {date_from} to {date_to}")
        print("")
    
    # In non-interactive environments, default to running all reports
    try:
        interactive = bool(getattr(sys, "stdin", None)) and sys.stdin.isatty()
    except Exception:
        interactive = False
    
    if interactive:
        try:
            print("Choose an option:")
            print("1. Run all reports now")
            print("2. Run diagnostics first")
            print("3. Exit")
            choice = input("Enter choice (1-3): ").strip()
        except (EOFError, RuntimeError):
            print("No interactive stdin detected; defaulting to run reports.")
            choice = "1"
    else:
        print("No interactive stdin detected; running all reports now.")
        choice = "1"
    
    if choice == "2":
        print("\nRunning QuickBooks diagnostics...")
        diagnostics = diagnose_quickbooks_connection(args.output)
        
        print_diagnostics_summary(diagnostics)
        
        print(f"\nDetailed report saved to: {args.output}")
        
        # Ask if they want to continue with reports
        try:
            continue_choice = input("\nDo you want to try running reports anyway? (y/n): ").lower().strip()
        except (EOFError, RuntimeError):
            continue_choice = "n"
        
        if continue_choice != "y":
            print("Exiting. Fix the issues above and try again.")
            return 0
        choice = "1"  # Continue to run reports
    
    if choice == "1":
        print("\nExporting all reports...")
        print("=" * 30)
        
        try:
            results, errors = export_all_reports(args.output, date_from, date_to)
            
            print("\n" + "=" * 50)
            print("FINAL RESULTS:")
            print("=" * 50)
            
            if results:
                print("\n✅ SUCCESSFUL REPORTS:")
                for key, result in results.items():
                    excel_status = "Yes" if result["excel_created"] else "No"
                    change_status = "Changed" if result["changed"] else "No Change"
                    print(f"   • {result['report_name']}: {result['rows']} rows, Excel: {excel_status}, {change_status}")
            
            if errors:
                print("\n❌ FAILED REPORTS:")
                for key, error in errors.items():
                    print(f"   • {key}: {error}")
                
                print(f"\n💡 TROUBLESHOOTING:")
                print(f"   • Check the log file in: {args.output}")
                print(f"   • Run diagnostics: quickbooks-autoreport --diagnose")
                print(f"   • Make sure QuickBooks Desktop and SDK are installed")
                
                return 1  # Return error code if any reports failed
            
            print(f"\n📁 Files saved to: {args.output}")
            if date_from and date_to:
                print(f"📅 Date range used: {date_from} to {date_to}")
            
            return 0  # Success
            
        except Exception as e:
            print(f"\n❌ FATAL ERROR: {e}")
            print("\nTROUBLESHOOTING:")
            print("1. Run diagnostics: quickbooks-autoreport --diagnose")
            print("2. Make sure QuickBooks Desktop is installed")
            print("3. Install QuickBooks SDK from Intuit Developer website")
            print("4. Run as Administrator")
            return 1
    
    elif choice == "3":
        print("Exiting.")
        return 0
    
    else:
        print("Invalid choice. Exiting.")
        print("Use --gui flag to launch the GUI interface.")
        return 1


def run_diagnostic_mode(args: argparse.Namespace) -> int:
    """Run in diagnostic mode.
    
    Args:
        args: Parsed command-line arguments
        
    Returns:
        Exit code (0 for success, 1 for error)
    """
    print("QuickBooks Auto Reporter - Diagnostic Mode")
    print("=" * 50)
    print("Running QuickBooks connectivity diagnostics...")
    print("")
    
    try:
        diagnostics = diagnose_quickbooks_connection(args.output)
        
        print_diagnostics_summary(diagnostics)
        
        print("")
        print(f"Detailed report saved to: {args.output}")
        print("Check 'quickbooks_diagnostics.json' and 'QuickBooks_Diagnostic_Report.xlsx'")
        
        # Return error code if there are issues
        if not diagnostics["quickbooks_installation"]["installed"] or not diagnostics["sdk_installation"]["installed"]:
            return 1
        
        conn_test = diagnostics.get("connectivity_test", {})
        com_success = conn_test.get("com_object_creation", {}).get("success", False)
        conn_success = conn_test.get("connection_test", {}).get("success", False)
        
        if not (com_success and conn_success):
            return 1
        
        return 0
        
    except Exception as e:
        print(f"❌ Diagnostic failed: {e}")
        return 1


def run_xml_test_mode(args: argparse.Namespace) -> int:
    """Run XML test mode.
    
    Args:
        args: Parsed command-line arguments
        
    Returns:
        Exit code (0 for success, 1 for error)
    """
    try:
        test_xml_generation()
        return 0
    except Exception as e:
        print(f"❌ XML test failed: {e}")
        return 1


def run_gui_mode(args: argparse.Namespace) -> int:
    """Run GUI mode.
    
    Args:
        args: Parsed command-line arguments
        
    Returns:
        Exit code (0 for success, 1 for error)
    """
    try:
        # Import GUI module here to avoid import errors if tkinter is not available
        from .gui import run_gui
        
        # Update settings if interval was specified
        if args.interval:
            settings = load_settings()
            settings["interval"] = args.interval
            save_settings(settings)
        
        # Override output directory if specified
        if args.output != DEFAULT_OUT_DIR:
            settings = load_settings()
            settings["output_dir"] = args.output
            save_settings(settings)
        
        run_gui()
        return 0
        
    except ImportError as e:
        print(f"❌ GUI mode not available: {e}")
        print("Make sure tkinter is installed and available.")
        return 1
    except Exception as e:
        print(f"❌ GUI failed to start: {e}")
        return 1


def main() -> int:
    """Main entry point for CLI application.
    
    Returns:
        Exit code (0 for success, 1 for error)
    """
    try:
        args = parse_arguments()
        
        # Determine mode and run appropriate function
        if args.diagnose:
            return run_diagnostic_mode(args)
        elif args.test_xml:
            return run_xml_test_mode(args)
        elif args.gui:
            return run_gui_mode(args)
        else:
            # Default to CLI mode, but check if we should default to GUI
            # Check if running as executable without console
            has_console = hasattr(sys, "stdin") and sys.stdin is not None
            is_executable = getattr(sys, "frozen", False)
            
            if is_executable or not has_console:
                # Running as executable or no console - launch GUI
                return run_gui_mode(args)
            else:
                # Run CLI mode
                return run_cli_mode(args)
                
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        return 1
    except Exception as e:
        print(f"\n❌ FATAL ERROR: {e}")
        if "--verbose" in sys.argv or "-v" in sys.argv:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())