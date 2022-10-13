import threading

from ui import TextTwistUI
from clock import Clock
from words import *

GAME_TIME = 120

class TextTwistGame:

    def __init__(self):
        self.__clock = Clock(GAME_TIME)
        self.__clock.add_observer(self)

        self.reset_game()
        self.__ui_callbacks = {}

    def get_score(self):
        return self.__score

    def is_level_passed(self):
        if self.__level_passed:
            return True
        else:
            return False

    def get_letters(self):
        return self.__letters

    def get_wordlist(self):
        return self.__wordlist

    def word_entry_is_valid(self, word):
        if word not in self.__solution_words and word in self.__wordlist:
            self.__solution_words.add(word)
            self.__score += len(word)
            if len(word) == 6:
                self.__level_passed = True
            return True
        else:
            return False

    def get_solution_words(self):
        return self.__solution_words

    def get_missing_solution_words(self):
        return self.__wordlist.difference(self.__solution_words)

    def get_clock(self):
        return self.__clock

    def run_clock(self):
        clock_thread = threading.Thread(target=self.__clock.run)
        clock_thread.start()

    def reset_clock(self):
        self.__clock.reset()

    def notify_clock_reached_zero(self):
        self.__ui_callbacks["clock_reached_zero"]() 

    def add_ui_callback(self, name, func):
        self.__ui_callbacks[name] = func

    def start_game(self):
        self.__level_passed = False
        self.__solution_words = set()
        self.__letters = list(get_six_letter_word())
        self.__wordlist = set(get_words_from_base_word("".join(self.__letters)))
        self.run_clock()

    def reset_game(self):
        self.__letters = []
        self.__wordlist = set()
        self.__solution_words = set()
        self.__score = 0
        self.__level_passed = False
        self.reset_clock()


def run_game_instance():
    ui = TextTwistUI()
    game = TextTwistGame()

    ui.add_game_object_to_ui(game)
    ui.start_mainloop()


if __name__ == "__main__":
    run_game_instance()

