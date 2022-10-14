from threading import Event
from tkinter import StringVar

from time import sleep

class Clock():

    def __init__(self, default_time=120):
        self.__string_var = StringVar()
        self.__default_time = default_time
        self.__seconds = default_time 
        self.set_string_var(self.__seconds)

        self.__observers = set()

        self.__exit = Event()

    def set_string_var(self, seconds):
        self.__string_var.set(self.get_time_string())

    def get_string_var(self):
        return self.__string_var

    def get_time(self):
        return self.__seconds

    def get_time_string(self):
        return "{}:{}".format(self.__seconds//60,
                (str)(self.__seconds%60).zfill(2))

    def run(self):
        self.reset()
        self.__exit.clear()
        while True:
            self.__seconds -= 1
            self.set_string_var(self.__seconds)
            if self.__seconds == 0:
                self.process_clock_reached_zero()
                break
            sleep(1)
            if self.__exit.is_set():
                self.__exit.clear()
                break

    def process_clock_reached_zero(self):
        for observer in self.__observers:
            observer.notify_clock_reached_zero()

    def set_to_zero(self):
        self.__seconds = 0
        self.set_string_var(self.__seconds)
        self.process_clock_reached_zero()

    def add_observer(self, observer):
        self.__observers.add(observer)

    def reset(self):
        self.__seconds = self.__default_time 
        self.set_string_var(self.__seconds)
        self.__exit.set()
