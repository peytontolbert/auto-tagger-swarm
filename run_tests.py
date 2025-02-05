#!/usr/bin/env python3
import unittest
import sys
from pathlib import Path

def run_tests():
    """Run all tests in the tests directory"""
    # Get the tests directory
    tests_dir = Path(__file__).parent / 'tests'
    
    # Create test loader
    loader = unittest.TestLoader()
    
    # Discover and run tests
    suite = loader.discover(str(tests_dir), pattern='test_*.py')
    
    # Create test runner
    runner = unittest.TextTestRunner(verbosity=2)
    
    # Run tests
    result = runner.run(suite)
    
    # Return appropriate exit code
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    sys.exit(run_tests()) 