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

    
    def test_get_six_letter_word(self):
        word = get_six_letter_word()

        self.assertTrue(len(word) == 6)


    def test_base_word_contains_test_word(self):
        self.assertTrue(base_word_contains_test_word("appear", "pear"))
        self.assertTrue(base_word_contains_test_word("crowds", "crows"))

        with self.assertRaises(ValueError):
            base_word_contains_test_word("", "help")
        with self.assertRaises(ValueError):
            base_word_contains_test_word("help", "")

if __name__ == "__main__":
    unittest.main()
