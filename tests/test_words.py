import unittest
import sys, os

sys.path.insert(0, os.path.abspath('..'))
from words import *

class TestWords(unittest.TestCase):

    def test_file_validation(self):
        file1 = "../wordlists/allwords.txt"
        file2 = "../wordlists/6letterwords.txt"
        file3 = ""
        file4 = True

        self.assertTrue(is_valid_file_name(file1))
        self.assertTrue(is_valid_file_name(file2))
        self.assertFalse(is_valid_file_name(file3))
        self.assertFalse(is_valid_file_name(file4))
              

if __name__ == "__main__":
    unittest.main()
