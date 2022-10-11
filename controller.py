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
        self.wordlist = []

    def get_letters(self):
        return self.letters

    def get_wordlist(self):
        return self.wordlist

    def reset_clock(self):
        self.clock.reset()

    def run_clock(self):
        clock_thread = threading.Thread(target=self.clock.run)
        clock_thread.start()

    def start_game(self):
        self.letters = list(get_six_letter_word())
        self.wordlist = get_words_from_base_word("".join(self.letters))
        run_clock()

    def reset_game(self):
        self.letters = []
        self.wordlist = []
        reset_clock()


if __name__ == "__main__":
    ui = TextTwistUI()
    game = TextTwistGame()

    ui.add_clock(game.clock,
            clock_run_callback=game.run_clock,
            clock_reset_callback=game.reset_clock)
    game.reset_clock()

    ui.set_letters()
    ui.start()
