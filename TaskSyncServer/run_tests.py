"""
Simple test harness for Task Sync Server.

This file discovers and runs all tests in the tests folder, then reports
whether the full test suite passed or failed.
"""

import unittest


def run_all_tests():
    """
    Discover and run all unit and integration tests.
    """
    loader = unittest.TestLoader()
    test_suite = loader.discover("tests")

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)

    return result.wasSuccessful()


if __name__ == "__main__":
    print("Running Task Sync Server test suite...")
    print("------------------------------------")

    success = run_all_tests()

    if success:
        print("\nAll tests passed.")
    else:
        print("\nSome tests failed.")