#!/usr/bin/env python3
"""
QuickBooks Order Exporter - Main Entry Point

This script provides a command-line interface for exporting QuickBooks
sales orders to Excel with Odoo enrichment.
"""

import sys
from pathlib import Path

# Add the package directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from quickbooks.cli import main

if __name__ == "__main__":
    try:
        excel_file, json_file = main()
        if excel_file:
            print(f"\n✅ Export completed successfully!")
            print(f"📊 Excel report: {excel_file}")
            if json_file:
                print(f"📄 JSON data: {json_file}")
        else:
            print("\n❌ Export failed. Check logs for details.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n👋 Export cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
