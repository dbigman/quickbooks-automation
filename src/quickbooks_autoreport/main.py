"""Main application entry point for QuickBooks Auto Reporter.

This module provides the primary entry point that routes to the appropriate
interface based on command-line arguments and execution context.
"""

import sys
import os

# Add the src directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from quickbooks_autoreport.cli import main as cli_main


def main() -> int:
    """Main application entry point.
    
    Returns:
        Exit code (0 for success, 1 for error)
    """
    return cli_main()


if __name__ == "__main__":
    sys.exit(main())