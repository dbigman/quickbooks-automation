"""Build script for QuickBooks Auto Reporter executable.

This script uses PyInstaller to create a standalone Windows executable
with all dependencies included.
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path


def clean_build_dirs():
    """Clean previous build directories."""
    dirs_to_clean = ["build", "dist", "__pycache__"]
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"Cleaning {dir_name}...")
            shutil.rmtree(dir_name)
    
    # Clean __pycache__ directories in subfolders
    for root, dirs, files in os.walk("."):
        for dir_name in dirs:
            if dir_name == "__pycache__":
                cache_path = os.path.join(root, dir_name)
                print(f"Cleaning {cache_path}...")
                shutil.rmtree(cache_path)


def create_spec_file():
    """Create PyInstaller spec file for the application."""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['src\\quickbooks_autoreport\\main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('src\\quickbooks_autoreport', 'quickbooks_autoreport'),
    ],
    hiddenimports=[
        'quickbooks_autoreport.config',
        'quickbooks_autoreport.services',
        'quickbooks_autoreport.adapters',
        'quickbooks_autoreport.utils',
        'quickbooks_autoreport.cli',
        'quickbooks_autoreport.gui',
        'tkinter',
        'tkinter.ttk',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'win32com',
        'win32com.client',
        'pythoncom',
        'pywintypes',
        'openpyxl',
        'xml.etree.ElementTree',
        'csv',
        'json',
        'hashlib',
        'datetime',
        'threading',
        'queue',
        'argparse',
        'winreg',
        'subprocess',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy',
        'scipy',
        'pandas',
        'jupyter',
        'notebook',
        'IPython',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='QuickBooksAutoReporter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if os.path.exists('icon.ico') else None,
    version='version_info.txt' if os.path.exists('version_info.txt') else None,
)
'''
    
    with open("QuickBooksAutoReporter.spec", "w", encoding="utf-8") as f:
        f.write(spec_content)
    
    print("Created PyInstaller spec file: QuickBooksAutoReporter.spec")


def create_version_info():
    """Create version info file for Windows executable."""
    version_info = '''# UTF-8
#
# For more details about fixed file info 'ffi' see:
# http://msdn.microsoft.com/en-us/library/ms646997.aspx
VSVersionInfo(
  ffi=FixedFileInfo(
# filevers and prodvers should be always a tuple with four items: (1, 2, 3, 4)
# Set not needed items to zero 0.
filevers=(2,0,0,0),
prodvers=(2,0,0,0),
# Contains a bitmask that specifies the valid bits 'flags'r
mask=0x3f,
# Contains a bitmask that specifies the Boolean attributes of the file.
flags=0x0,
# The operating system for which this file was designed.
# 0x4 - NT and there is no need to change it.
OS=0x4,
# The general type of file.
# 0x1 - the file is an application.
fileType=0x1,
# The function of the file.
# 0x0 - the function is not defined for this fileType
subtype=0x0,
# Creation date and time stamp.
date=(0, 0)
),
  kids=[
StringFileInfo(
  [
  StringTable(
    u'040904B0',
    [StringStruct(u'CompanyName', u'Gasco Industrial'),
    StringStruct(u'FileDescription', u'QuickBooks Auto Reporter - Automated report generation with change detection'),
    StringStruct(u'FileVersion', u'2.0.0.0'),
    StringStruct(u'InternalName', u'QuickBooksAutoReporter'),
    StringStruct(u'LegalCopyright', u'Copyright © 2025 Gasco Industrial'),
    StringStruct(u'OriginalFilename', u'QuickBooksAutoReporter.exe'),
    StringStruct(u'ProductName', u'QuickBooks Auto Reporter'),
    StringStruct(u'ProductVersion', u'2.0.0.0')])
  ]), 
VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
'''
    
    with open("version_info.txt", "w", encoding="utf-8") as f:
        f.write(version_info)
    
    print("Created version info file: version_info.txt")


def install_dependencies():
    """Install required dependencies for building."""
    dependencies = [
        "pyinstaller",
        "pywin32",
        "openpyxl",
    ]
    
    print("Installing build dependencies...")
    for dep in dependencies:
        try:
            print(f"Installing {dep}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
        except subprocess.CalledProcessError as e:
            print(f"Failed to install {dep}: {e}")
            return False
    
    return True


def build_executable():
    """Build the executable using PyInstaller."""
    print("Building executable with PyInstaller...")
    
    try:
        # Run PyInstaller with the spec file
        subprocess.check_call([
            sys.executable, "-m", "PyInstaller",
            "--clean",
            "--noconfirm",
            "QuickBooksAutoReporter.spec"
        ])
        
        print("Build completed successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")
        return False


def create_installer_script():
    """Create a simple NSIS installer script."""
    nsis_script = '''; QuickBooks Auto Reporter Installer Script

!define APPNAME "QuickBooks Auto Reporter"
!define VERSION "2.0.0.0"
!define PUBLISHER "Gasco Industrial"
!define EXECUTABLE "QuickBooksAutoReporter.exe"

; Include Modern UI
!include "MUI2.nsh"

; General
Name "${APPNAME}"
OutFile "${APPNAME}_Setup_${VERSION}.exe"
InstallDir "$PROGRAMFILES\\${APPNAME}"
InstallDirRegKey HKLM "Software\\${APPNAME}" "InstallPath"
RequestExecutionLevel admin

; Interface Settings
!define MUI_ABORTWARNING
!define MUI_ICON "${EXECUTABLE}"

; Pages
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "LICENSE.txt"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

; Languages
!insertmacro MUI_LANGUAGE "English"

; Installer Sections
Section "MainSection" SEC01
  SetOutPath "$INSTDIR"
  File "dist\\${EXECUTABLE}"
  
  ; Create uninstaller
  WriteUninstaller "$INSTDIR\\Uninstall.exe"
  
  ; Create Start Menu shortcuts
  CreateDirectory "$SMPROGRAMS\\${APPNAME}"
  CreateShortCut "$SMPROGRAMS\\${APPNAME}\\${APPNAME}.lnk" "$INSTDIR\\${EXECUTABLE}"
  CreateShortCut "$SMPROGRAMS\\${APPNAME}\\Uninstall.lnk" "$INSTDIR\\Uninstall.exe"
  
  ; Write registry keys
  WriteRegStr HKLM "Software\\${APPNAME}" "InstallPath" "$INSTDIR"
  WriteRegStr HKLM "Software\\${APPNAME}" "Version" "${VERSION}"
  WriteRegStr HKLM "Software\\${APPNAME}" "Publisher" "${PUBLISHER}"
  
  ; Write uninstaller registry keys
  WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APPNAME}" "DisplayName" "${APPNAME}"
  WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APPNAME}" "UninstallString" "$INSTDIR\\Uninstall.exe"
  WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APPNAME}" "DisplayVersion" "${VERSION}"
  WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APPNAME}" "Publisher" "${PUBLISHER}"
  WriteRegDWORD HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APPNAME}" "NoModify" 1
  WriteRegDWORD HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APPNAME}" "NoRepair" 1
SectionEnd

; Uninstaller Section
Section "Uninstall"
  Delete "$INSTDIR\\${EXECUTABLE}"
  Delete "$INSTDIR\\Uninstall.exe"
  
  Delete "$SMPROGRAMS\\${APPNAME}\\${APPNAME}.lnk"
  Delete "$SMPROGRAMS\\${APPNAME}\\Uninstall.lnk"
  RMDir "$SMPROGRAMS\\${APPNAME}"
  
  RMDir "$INSTDIR"
  
  DeleteRegKey HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APPNAME}"
  DeleteRegKey HKLM "Software\\${APPNAME}"
SectionEnd
'''
    
    with open("installer.nsi", "w", encoding="utf-8") as f:
        f.write(nsis_script)
    
    print("Created NSIS installer script: installer.nsi")


def create_readme():
    """Create README file for the distribution."""
    readme_content = '''# QuickBooks Auto Reporter v2.0

## Overview

QuickBooks Auto Reporter is a powerful automation tool that generates QuickBooks reports
with continuous polling, change detection, and professional export capabilities.

## Features

- **Automated Report Generation**: Supports 9 different QuickBooks report types
- **Continuous Polling**: Configurable intervals (5, 15, 30, 60 minutes)
- **Change Detection**: Automatic snapshot creation when data changes
- **Professional Export**: CSV and Excel with corporate styling
- **Multiple Interfaces**: GUI and CLI modes
- **Comprehensive Diagnostics**: Built-in troubleshooting tools

## Supported Reports

1. Open Sales Orders by Item
2. Profit & Loss (Standard and Detail)
3. Sales by Item (Summary and Detail)
4. Sales by Rep Detail
5. Purchase by Vendor Detail
6. AP Aging Detail
7. AR Aging Detail

## Requirements

- Windows 10 or later
- QuickBooks Desktop (any recent version)
- QuickBooks SDK (download from Intuit Developer website)
- Microsoft .NET Framework 4.7.2 or later

## Installation

1. Download the QuickBooksAutoReporter_Setup.exe file
2. Run the installer as Administrator
3. Follow the installation wizard
4. Launch the application from Start Menu

## Quick Start

1. **Install QuickBooks SDK**: Download from Intuit Developer website
2. **Launch Application**: Run QuickBooks Auto Reporter
3. **Configure Output**: Select your preferred output folder
4. **Set Date Range**: Choose the date range for reports
5. **Start Automation**: Click "Start Auto" to begin continuous polling

## Troubleshooting

If you encounter connection issues:

1. Run the application with `--diagnose` flag
2. Check the diagnostic report in the output folder
3. Ensure QuickBooks Desktop is installed and running
4. Verify QuickBooks SDK is properly installed
5. Run the application as Administrator

## Command Line Usage

The application supports several command-line modes:

```bash
# Launch GUI
QuickBooksAutoReporter.exe --gui

# Run diagnostics
QuickBooksAutoReporter.exe --diagnose

# Export reports immediately
QuickBooksAutoReporter.exe --output C:\\Reports

# Custom date range
QuickBooksAutoReporter.exe --date-from 2025-01-01 --date-to 2025-01-31

# Test XML generation
QuickBooksAutoReporter.exe --test-xml
```

## Support

For technical support and documentation, please contact:
- Email: support@gascoindustrial.com
- Documentation: Check the output folder for generated reports and logs

## License

Copyright © 2025 Gasco Industrial. All rights reserved.
'''
    
    with open("README_DISTRO.txt", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print("Created distribution README: README_DISTRO.txt")


def main():
    """Main build process."""
    print("QuickBooks Auto Reporter - Build Script")
    print("=" * 50)
    
    # Check if we're on Windows
    if sys.platform != "win32":
        print("Error: This build script is designed for Windows only.")
        return 1
    
    # Clean previous builds
    clean_build_dirs()
    
    # Install dependencies
    if not install_dependencies():
        print("Failed to install dependencies. Aborting build.")
        return 1
    
    # Create build files
    create_spec_file()
    create_version_info()
    create_installer_script()
    create_readme()
    
    # Build executable
    if not build_executable():
        print("Build failed. Check the error messages above.")
        return 1
    
    # Verify executable was created
    exe_path = Path("dist/QuickBooksAutoReporter.exe")
    if exe_path.exists():
        print(f"✅ Executable created: {exe_path.absolute()}")
        print(f"   Size: {exe_path.stat().st_size / (1024*1024):.1f} MB")
    else:
        print("❌ Executable not found after build")
        return 1
    
    print("\n" + "=" * 50)
    print("BUILD COMPLETED SUCCESSFULLY!")
    print("=" * 50)
    print("\nNext steps:")
    print("1. Test the executable: dist\\QuickBooksAutoReporter.exe")
    print("2. Create installer (optional): makensis installer.nsi")
    print("3. Distribute the executable and installer")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())