# This file ensures that Python treats the tests directory as a package
# It can be used to set up any global test configurations or imports
import sys
import os

# Add the parent directory to Python path to import app modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
