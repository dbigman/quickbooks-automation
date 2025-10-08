"""Test runner for QuickBooks Auto Reporter.

This script runs all tests and provides a summary of results.
"""

import sys
import os
import unittest
import time
from io import StringIO

# Add the src directory to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))


def discover_and_run_tests():
    """Discover and run all tests in the tests directory."""
    # Discover tests
    loader = unittest.TestLoader()
    start_dir = 'tests'
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # Create test runner with detailed output
    stream = StringIO()
    runner = unittest.TextTestRunner(
        stream=stream,
        verbosity=2,
        descriptions=True,
        failfast=False
    )
    
    # Run tests
    print("Running QuickBooks Auto Reporter Tests")
    print("=" * 50)
    print("Discovering tests in 'tests' directory...")
    
    start_time = time.time()
    result = runner.run(suite)
    end_time = time.time()
    
    # Get output
    output = stream.getvalue()
    
    # Print results
    print("\n" + "=" * 50)
    print("TEST RESULTS SUMMARY")
    print("=" * 50)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped) if hasattr(result, 'skipped') else 0}")
    print(f"Time: {end_time - start_time:.2f} seconds")
    
    if result.failures:
        print(f"\nFAILURES ({len(result.failures)}):")
        for test, traceback in result.failures:
            print(f"  - {test}")
    
    if result.errors:
        print(f"\nERRORS ({len(result.errors)}):")
        for test, traceback in result.errors:
            print(f"  - {test}")
    
    # Print detailed output
    print("\n" + "=" * 50)
    print("DETAILED TEST OUTPUT")
    print("=" * 50)
    print(output)
    
    # Return appropriate exit code
    if result.failures or result.errors:
        print("\n❌ TESTS FAILED")
        return 1
    else:
        print("\n✅ ALL TESTS PASSED")
        return 0


def run_specific_test(test_name):
    """Run a specific test module.
    
    Args:
        test_name: Name of the test module (without .py extension)
    """
    test_module = f"tests.{test_name}"
    
    try:
        # Import the test module
        module = __import__(test_module, fromlist=[test_name])
        
        # Create test suite
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromModule(module)
        
        # Run tests
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        return 0 if result.wasSuccessful() else 1
        
    except ImportError as e:
        print(f"❌ Could not import test module '{test_name}': {e}")
        return 1


def list_available_tests():
    """List all available test modules."""
    import os
    
    print("Available test modules:")
    print("=" * 30)
    
    test_dir = 'tests'
    if not os.path.exists(test_dir):
        print("No tests directory found.")
        return
    
    for file in os.listdir(test_dir):
        if file.startswith('test_') and file.endswith('.py'):
            test_name = file[:-3]  # Remove .py extension
            print(f"  - {test_name}")


def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        
        if arg == "--list":
            list_available_tests()
            return 0
        elif arg.startswith("test_"):
            return run_specific_test(arg)
        elif arg == "--help":
            print("Usage: python run_tests.py [test_name|--list|--help]")
            print("")
            print("Options:")
            print("  test_name    Run specific test module (e.g., test_config)")
            print("  --list       List all available test modules")
            print("  --help       Show this help message")
            print("")
            print("If no arguments are provided, all tests will be run.")
            return 0
        else:
            print(f"Unknown argument: {arg}")
            print("Use --help for usage information.")
            return 1
    else:
        # Run all tests
        return discover_and_run_tests()


if __name__ == "__main__":
    sys.exit(main())