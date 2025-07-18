# Import system library
import sys
sys.path.append('.')
sys.path.append('./pytest_basics/')


# load test environment variables
import os
from dotenv import load_dotenv

# Set working directory and filename
current_filename = os.path.basename(__file__) # the name of the current file
current_dirname = os.path.dirname(__file__) # the name of the current directory
env_file = os.path.join(current_dirname, 'test.env')

print('File :\n', current_filename)
print('Directory :\n', current_dirname)
print('Test variables :\n', env_file)

# load test.env file
load_dotenv(env_file)


# load test system file
def test_system_file():
    # Test system_file.py
    print('Test system file')

