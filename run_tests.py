# DO NOT MODIFY UNLESS NECESSARY

import unittest
from gradescope_utils.autograder_utils.json_test_runner import JSONTestRunner

if __name__ == '__main__':
    suite = unittest.defaultTestLoader.discover('tests') # Finds all python files with prefix test_ in tests directory and load the test methods in them as unittest.TestCase objects
    with open('/autograder/results/results.json', 'w') as f:
        JSONTestRunner(visibility='visible', stream=f).run(suite) # Run all tests and store results in expected JSON format
