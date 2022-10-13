from threading import Event
from tkinter import StringVar

from time import sleep

class Clock():

    def __init__(self):
        self.string_var = StringVar()
        self.seconds = 120
        self.set_string_var(self.seconds)
        self.exit = Event()

    def set_string_var(self, seconds):
        self.string_var.set(self.get_time_string(self.seconds))

    def get_string_var(self):
        return self.string_var

    def get_time(self):
        return self.seconds

    def get_time_string(self, seconds):
        return "{}:{}".format(seconds//60, (str)(seconds%60).zfill(2))

    def run(self):
        if self.exit.is_set():
            self.exit.clear()
        while True:
            self.seconds -= 1
            self.set_string_var(self.seconds)
            sleep(1)
            if self.exit.is_set():
                self.exit.clear()
                break

    def reset(self):
        self.seconds = 120
        self.set_string_var(self.seconds)
        self.exit.set()
