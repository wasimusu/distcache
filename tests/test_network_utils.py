"""
Tests distcache/utils.py

Testing objective:
    Is anything lost while transferring between server and clients.
    Send and receive objects. If you what to expect, you can test it.

Testing idea:
    The clients and servers are going to send and receive things and they would know what to expect as well.
    Send and receive different types of things.
    Fibonacci series with numbers
    Squares of 0.9 for k iteration
    Send and receive all letters
    Echo servers. Repeat 1000 iterations to see if the message changes.
    Echo servers but for floats
"""

import unittest
from distcache import utils


class Server:
    def __init__(self):
        pass

    def send(self):
        pass


class Client:
    def __init__(self):
        pass

    def send(self):
        pass


class NetworkUtilsTest(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
