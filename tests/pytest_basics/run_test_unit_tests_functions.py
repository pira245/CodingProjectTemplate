import os
import pytest
import logging
##############################################################################################
"""
    Testing methods and classes for functions unit tests
"""
##############################################################################################
# Import all test files
import core
import core.mytestunity.system_file as system_file
##############################################################################################

def test_system_file():
    # Test system_file.py
    system_file.test_system_file()

if __name__ == "__main__":
    # Run all tests available
    
    pytest.main(["-v", __file__])