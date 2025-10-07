#!/usr/bin/env python3
"""
Example usage of the MO Cost Analysis tool
"""

import subprocess
import sys
from datetime import datetime, timedelta


def run_mo_cost_analysis():
    """Example of running the MO cost analysis tool"""

    print("=== Manufacturing Order Cost Analysis Example ===\n")

    # Example 1: Interactive mode
    print("1. Interactive Mode (will prompt for dates):")
    print("   python scripts/quickbooks/mo_costs.py")
    print()

    # Example 2: Command line with specific dates
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

    print("2. Command Line Mode (last 30 days):")
    print(
        f"   python scripts/quickbooks/mo_costs.py --start-date {start_date} --end-date {end_date}"
    )
    print()

    # Example 3: Console output
    print("3. Console Output Mode:")
    print(
        f"   python scripts/quickbooks/mo_costs.py --start-date {start_date} --end-date {end_date} --console"
    )
    print()

    # Example 4: JSON output
    print("4. JSON Output Mode:")
    print(
        f"   python scripts/quickbooks/mo_costs.py --start-date {start_date} --end-date {end_date} --json"
    )
    print()

    # Ask user if they want to run an example
    choice = (
        input("Would you like to run the interactive mode now? (y/n): ")
        .strip()
        .lower()
    )

    if choice == "y":
        try:
            # Run the script in interactive mode
            subprocess.run(
                [sys.executable, "scripts/quickbooks/mo_costs.py"], check=True
            )
        except subprocess.CalledProcessError as e:
            print(f"Error running script: {e}")
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
    else:
        print("You can run any of the examples above manually.")


if __name__ == "__main__":
    run_mo_cost_analysis()
