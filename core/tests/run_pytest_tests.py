import os
import pytest
import logging
##############################################################################################
"""
    Testing with pytest
"""
##############################################################################################
from system_file import TestEnvironmentSetup
##############################################################################################

class RunPytestTests(TestEnvironmentSetup):
    """Handles pytest test collection """

    @pytest.fixture(autouse=True)
    def setup(self):
        self.test_env = super().load_environment()

    
    def run_all_tests(self):
    # Run all tests available
        print("Running tests...")
        pytest.main(["-v", __file__])

def test_number_1():
    # Test system_file.py
    print("This is my first test")

if __name__ == "__main__":
    # Load Current Test Unit for pytest collection:
    TestUnit = RunPytestTests()
    TestUnit.load_environment()
    # Run all tests available
    TestUnit.run_all_tests()