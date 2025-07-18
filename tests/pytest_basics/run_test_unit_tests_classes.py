import os
import pytest
import logging
##############################################################################################
"""
    Testing methods and classes for classes unit tests
"""
##############################################################################################
# Import all test files
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../mytestunity/pytest_basics/library')))

#from library.Module import Class
#from library.Module import Class
##############################################################################################

def test_1():
    # Test system_file.py
    print("Test 1")



if __name__ == "__main__":
    # Run all tests available

    pytest.main(["-v", __file__])