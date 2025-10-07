from __future__ import annotations

import os
import sys
from datetime import datetime
from typing import Optional, Tuple

from .excel_export import generate_quickbooks_excel_report


def get_quickbooks_file_path() -> str:
    print("🏭 QUICKBOOKS OPEN SALES ORDERS REPORT GENERATOR")
    print("=" * 70)
    print(f"📅 Report Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🔗 Data Source: QuickBooks CSV Export")
    print("📋 Report Type: Open Sales Orders")
    print("=" * 70)

    default_files = [
        f
        for f in os.listdir(".")
        if f.lower().endswith(".csv")
        and "open" in f.lower()
        and "so" in f.lower()
    ]
    if default_files:
        print(
            f"\n📁 Found {len(default_files)} potential QuickBooks CSV file(s):"
        )
        for i, filename in enumerate(default_files, 1):
            print(f"   {i}. {filename}")
        print(f"   {len(default_files) + 1}. Enter custom file path")
        while True:
            try:
                choice = input(
                    f"\n🔢 Select file (1-{len(default_files) + 1}): "
                ).strip()
                if choice.isdigit():
                    n = int(choice)
                    if 1 <= n <= len(default_files):
                        return default_files[n - 1]
                    if n == len(default_files) + 1:
                        break
                print(
                    f"❌ Invalid choice. Please enter 1-{len(default_files) + 1}"
                )
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                sys.exit(0)

    while True:
        try:
            file_path = (
                input("\n📂 Enter QuickBooks CSV file path: ")
                .strip()
                .strip("\"'")
            )
            if not file_path:
                print("❌ Please enter a file path")
                continue
            if os.path.exists(file_path):
                print(f"✅ File found: {file_path}")
                return file_path
            print(f"❌ File not found: {file_path}")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            sys.exit(0)


def main() -> Tuple[Optional[str], Optional[str]]:
    file_path = get_quickbooks_file_path()
    return generate_quickbooks_excel_report(file_path)


if __name__ == "__main__":
    main()
