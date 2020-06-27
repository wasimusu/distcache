"""
Tests distcache/logger.py

Testing objective:
    Is there any data corruption?
    Are all the objects logged properly.

Testing ideas:
    Read from a file. Write to actual_log.txt. Compare it to expected_log.txt
    Generate file of different types.
    Do lots of iterations.
"""
import unittest
from distcache import logger


class LoggerTest(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
