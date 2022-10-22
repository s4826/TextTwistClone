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
        base_contains_test = base_word_contains_test_word
        self.assertTrue(base_contains_test("appear", "pear"))
        self.assertTrue(base_contains_test("crowds", "crows"))
        self.assertFalse(base_contains_test("", "help"))
        self.assertFalse(base_contains_test("help", ""))

if __name__ == "__main__":
    unittest.main()
