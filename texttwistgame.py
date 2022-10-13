import threading
import random

from tkinter.constants import DISABLED, NORMAL

from ui import TextTwistUI
from clock import Clock
from words import *


class TextTwistGame:

    def __init__(self):
        self.clock = Clock()
        self.letters = []
        self.wordlist = set()
        self.solution_words = set()

    def get_letters(self):
        return self.letters

    def get_wordlist(self):
        return self.wordlist

    def word_entry_is_valid(self, word):
        if word not in self.solution_words and word in self.wordlist:
            self.solution_words.add(word)
            if len(word) == 6:
                self.level_passed = True
            return True
        else:
            return False

    def get_solution_words(self):
        return self.solution_words

    def get_clock(self):
        return self.clock

    def run_clock(self):
        clock_thread = threading.Thread(target=self.clock.run)
        clock_thread.start()

    def reset_clock(self):
        self.clock.reset()

    def process_clock_reached_zero(self):
        pass

    def start_game(self):
        self.level_passed = False
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

    ui.add_game_object_to_ui(game)
    ui.start_mainloop()
