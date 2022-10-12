import threading
import random

from tkinter.constants import DISABLED, NORMAL

from ui import TextTwistUI
from clock import Clock
from words import *

class TextTwistGame:
    """
    Class to encapsulate Text Twist game
    """

    def __init__(self):
        self.clock = Clock()
        self.letters = []
        self.wordlist = set()
        self.entered_words = set()

    def get_letters(self):
        return self.letters

    def get_wordlist(self):
        return self.wordlist

    def validate_word_entry(self, word):
        if word in self.wordlist:
            self.entered_words.add(word)
            return True
        else:
            return False

    def run_clock(self):
        clock_thread = threading.Thread(target=self.clock.run)
        clock_thread.start()

    def reset_clock(self):
        self.clock.reset()

    def start_game(self):
        self.letters = list(get_six_letter_word())
        self.wordlist = set(get_words_from_base_word("".join(self.letters)))
        self.run_clock()

    def reset_game(self):
        self.letters = []
        self.wordlist = set() 
        self.reset_clock()


if __name__ == "__main__":
    ui = TextTwistUI()
    game = TextTwistGame()

    ui.add_clock(game.clock)
    ui.add_game_object_to_ui(game)
    ui.start()
