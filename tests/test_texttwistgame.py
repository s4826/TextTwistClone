import unittest
import sys
import os
import tkinter as tk


sys.path.insert(0, os.path.abspath('..'))
from texttwistgame import TextTwistGame


class GameTest(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()

    def test_level_passed(self):
        game = TextTwistGame()
        game._TextTwistGame__wordlist = ["swords", "words"]

        game.word_entry_is_valid("swords")
        self.assertTrue(game.level_passed())
        
        game = TextTwistGame()
        game._TextTwistGame__wordlist = ["swords", "sword", "word"]

        game.word_entry_is_valid("sword")
        self.assertFalse(game.level_passed())

        game.word_entry_is_valid("word")
        self.assertFalse(game.level_passed())

    def tearDown(self):
        self.root.destroy()


if __name__ == "__main__":
    unittest.main()
