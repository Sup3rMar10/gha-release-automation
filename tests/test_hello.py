import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from hello import greet


class HelloTests(unittest.TestCase):
    def test_greet(self):
        self.assertEqual(greet("ada"), "hello, ada")


if __name__ == "__main__":
    unittest.main()
