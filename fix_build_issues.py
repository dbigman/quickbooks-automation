#!/usr/bin/env python3
"""
Fix package conflicts for PyInstaller build
This script cleans up problematic package installations
"""

import os
import subprocess
import sys


def run_pip_command(cmd):
    """Run a pip command and return success status"""
    try:
        result = subprocess.run([sys.executable, "-m", "pip"] + cmd, 
                              capture_output=True, text=True, check=True)
        print(f"✅ {' '.join(cmd)}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {' '.join(cmd)} failed: {e.stderr}")
        return False

def fix_package_conflicts():
    """Fix known package conflicts"""
    print("🔧 Fixing PyInstaller package conflicts...")
    print("=" * 50)
    
    # Step 1: Uninstall problematic packages
    problematic_packages = [
        "pkg-resources",
        "jaraco.text", 
        "jaraco.context",
        "jaraco.functools",
        "backports.tarfile",
        "importlib-metadata"
    ]
    
    print("\n📦 Removing problematic packages...")
    for package in problematic_packages:
        print(f"Removing {package}...")
        subprocess.run([sys.executable, "-m", "pip", "uninstall", package, "-y"], 
                      capture_output=True)
    
    # Step 2: Reinstall PyInstaller cleanly
    print("\n🔨 Reinstalling PyInstaller...")
    run_pip_command(["uninstall", "pyinstaller", "-y"])
    run_pip_command(["install", "pyinstaller>=5.0", "--no-deps", "--force-reinstall"])
    
    # Step 3: Install only essential dependencies
    essential_packages = [
        "pywin32>=305",
        "openpyxl>=3.0.0", 
        "altgraph",
        "pefile;sys_platform=='win32'",
        "pyinstaller-hooks-contrib>=2021.4"
    ]
    
    print("\n📦 Installing essential packages...")
    for package in essential_packages:
        run_pip_command(["install", package])
    
    print("\n✅ Package cleanup completed!")
    print("\nYou can now try building with:")
    print("  python build_exe_simple.py")
    print("  or")  
    print("  build_exe_simple.bat")

def main():
    print("🚀 QuickBooks Auto Reporter - Package Conflict Fixer")
    print("=" * 55)
    
    # Check if we're in the right directory
    if not os.path.exists("quickbooks_autoreport.py"):
        print("❌ Error: quickbooks_autoreport.py not found!")
        print("Please run this script from the same directory as your QuickBooks script.")
        return False
    
    try:
        fix_package_conflicts()
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    input("\nPress Enter to exit...")
    sys.exit(0 if success else 1)