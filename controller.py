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

    def reset_clock(self):
        self.clock.reset()

    def run_clock(self):
        clock_thread = threading.Thread(target=self.clock.run)
        clock_thread.start()


if __name__ == "__main__":
    ui = TextTwistUI()
    game = TextTwistGame()

    ui.add_clock(game.clock,
            clock_run_callback=game.run_clock,
            clock_reset_callback=game.reset_clock)
    game.reset_clock()

    ui.set_letters()
    ui.start()
