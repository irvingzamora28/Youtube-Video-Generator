#!/usr/bin/env python
"""
Test runner for the video generation project using pytest.
"""
import sys
import subprocess

def run_tests():
    """Run all tests using pytest."""
    print("Running tests with pytest...")
    
    # Run pytest with verbose output
    result = subprocess.run(["pytest", "-v"], capture_output=True, text=True)
    
    # Print the output
    print(result.stdout)
    
    if result.stderr:
        print("Errors:")
        print(result.stderr)
    
    # Return the result
    return result.returncode == 0

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
