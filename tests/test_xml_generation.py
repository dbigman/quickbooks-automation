#!/usr/bin/env python3
"""
Test script for QuickBooks XML generation
Tests the XML generation against working examples
"""

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

from quickbooks_autoreport import test_xml_generation

if __name__ == "__main__":
    test_xml_generation()
