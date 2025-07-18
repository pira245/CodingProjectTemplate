import os
import pytest
import logging
##############################################################################################
"""
    Testing with pytest
"""
##############################################################################################
# Import all test files
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import mytestunity.system_file as system_file
import mytestunity.pytest_basics.run_test_unit_tests_classes as run_test_unit_tests_classes
import mytestunity.pytest_basics.run_test_integration_tests as run_test_integration_tests
##############################################################################################

def test_system_file():
    # Test system_file.py
    system_file.test_system_file()


if __name__ == "__main__":
    # Run all tests available
    print("Running tests...")
    pytest.main(["-v", __file__])
   