#!/bin/bash

# Ensure script is run from backend directory
cd "$(dirname "$0")"

# Activate virtual environment
source venv/bin/activate

# Print Python and pip versions
echo "Python version:"
python3 --version

echo "Pip version:"
pip --version

# Install dependencies with verbose output
echo "Installing dependencies..."
pip install -r requirements.txt -v

# Print installed packages
echo "Installed packages:"
pip list

# Run tests with verbose output and catch any errors
echo "Running tests..."
python3 -m pytest tests/ -v

# Capture the exit code
TEST_EXIT_CODE=$?

# Print exit code for debugging
echo "Test Exit Code: $TEST_EXIT_CODE"

# Print test summary
echo "Test Summary:"
pytest --collect-only tests/

# Print detailed test results
echo "Detailed Test Results:"
pytest tests/ -v

# Exit with the test result
exit $TEST_EXIT_CODE
