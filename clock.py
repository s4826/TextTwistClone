from threading import Event
from tkinter import StringVar

from time import sleep

class Clock():

    def __init__(self, default_time=120):
        self.string_var = StringVar()
        self.default_time = default_time
        self.seconds = default_time 
        self.set_string_var(self.seconds)

        self.observers = set()

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
        self.reset()
        self.exit.clear()
        while True:
            self.seconds -= 1
            self.set_string_var(self.seconds)
            if self.seconds == 0:
                self.process_clock_reached_zero()
                break
            sleep(1)
            if self.exit.is_set():
                self.exit.clear()
                break

    def process_clock_reached_zero(self):
        for observer in self.observers:
            observer.notify_clock_reached_zero()

    def add_observer(self, observer):
        self.observers.add(observer)

    def reset(self):
        self.seconds = self.default_time 
        self.set_string_var(self.seconds)
        self.exit.set()


    def add_queue(self, q):
        self.q = q
