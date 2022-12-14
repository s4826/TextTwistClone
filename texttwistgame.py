import threading

from clock import Clock
from words import *


GAME_TIME = 120

class TextTwistGame:
    """
    Main game class

    Handles all events/variables associated with the state of a
    Text Twist game/level, including wordlists, clock management,
    and level completion status.
    """

    def __init__(self):
        """
        Create a game instance
        """
        self.clock = Clock(GAME_TIME)
        self.clock.observers.add(self.notify_clock_reached_zero)

        self.reset_game()
        self.ui_callbacks = {}


    def get_score(self):
        """
        Get the current game score.
        """
        return self.__score


    def get_letters(self):
        """
        Return the current letters of the game instance.
        """
        return self.__letters


    def get_wordlist(self):
        """
        Return the list of all words that can be made with
        the current game letters.
        """
        return self.__wordlist


    def word_entry_is_valid(self, word):
        """
        Check if 'word' is a valid entry, based on '__wordlist'.
        If so, add it to the solution set, check level completion
        conditions, and return True. Otherwise, return False.

        Note: Calling this method with words that are already in
        the current solution set (user-entered words) will
        return False.
        """
        if word not in self.__entered_words and word in self.__wordlist:
            self.__entered_words.add(word)
            self.__score += len(word)

            # got six-letter word, level passed
            if len(word) == 6:
                self.__level_passed = True

            # solution word set contains all words from wordlist
            # puzzle finished before time, set clock to zero
            if len(self.__entered_words) == len(self.__wordlist):
                self.clock.set_to_zero()

            return True
        else:
            return False


    def get_missing_solution_words(self):
        """
        Return the words from the wordlist that have not been
        entered into the solution set yet.
        """
        return self.__wordlist.difference(self.__entered_words)


    def level_passed(self):
        """
        Return the completion status of the current level.
        """
        if self.__level_passed:
            return True
        else:
            return False


    def run_clock(self):
        """
        Run the game clock in its own thread.
        """
        clock_thread = threading.Thread(target=self.clock.run,
                                        name="clock_thread")

        # If a clock thread is already running, we don't want to
        # start another one. Simply reset (restart) the timer
        # for the current thread.
        if (threading.active_count() > 1):
            self.clock.reset_while_running()
        else:
            clock_thread.start()


    def reset_clock(self):
        """
        Reset the game clock.
        """
        self.clock.reset()


    def notify_clock_reached_zero(self):
        """
        Notify all ui listeners that the clock reached zero.
        """
        for function in self.ui_callbacks.values():
            function()


    def add_ui_callback(self, name, func):
        """
        Add a ui function as a listener for game events.
        """
        self.ui_callbacks[name] = func


    def start_game(self):
        """
        Start a game level. Reset instance variables associated with
        a level and run the clock.
        """
        self.__level_passed = False
        self.__entered_words = set()
        self.__letters = list(get_six_letter_word())
        self.__wordlist = set(get_words_from_base_word("".join(self.__letters)))
        self.run_clock()


    def reset_game(self):
        """
        Reset all instance variables of the game to their starting
        state. This is a hard reset that will zero the score.
        """
        self.__letters = []
        self.__wordlist = set()
        self.__entered_words = set()
        self.__score = 0
        self.__level_passed = False
        self.reset_clock()

