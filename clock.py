from threading import Event
from tkinter import StringVar

from time import sleep

class Clock():

    def __init__(self, default_time=120):
        """
        Initialize a clock with a StringVar (used by tkinter),
        a default time, an observers set, and an exit event.
        """
        self.__string_var = StringVar()
        self.__default_time = default_time
        self.__seconds = default_time 
        self.set_string_var(self.__seconds)

        self.__observers = set()

        self.__exit = Event()

    def set_string_var(self, seconds):
        """
        Set '__string_var' to the appropriate time string based
        on the argument 'seconds.'
        """
        self.__string_var.set(str(self))

    def get_string_var(self):
        """
        Return a reference to instance variable '__string_var'
        """
        return self.__string_var

    def get_time(self):
        """
        Get current time on the clock in seconds
        """
        return self.__seconds

    def run(self):
        """
        Start the clock
        """
        self.reset()
        self.__exit.clear()
        while True:
            if self.__exit.is_set():
                self.__exit.clear()
                break
            self.__seconds -= 1
            self.set_string_var(self.__seconds)
            if self.__seconds == 0:
                self.process_clock_reached_zero()
                break
            sleep(1)

    def process_clock_reached_zero(self):
        """
        Notify all observers that the clock reached zero
        """
        for observer in self.__observers:
            observer.notify_clock_reached_zero()

    def set_to_zero(self):
        """
        Set the clock to zero
        """
        self.__seconds = 0
        self.__exit.set()
        self.set_string_var(self.__seconds)
        self.process_clock_reached_zero()

    def add_observer(self, observer):
        """
        Add an observer for the clock
        """
        self.__observers.add(observer)

    def reset(self):
        """
        Reset the clock to the default time, and set the
        exit event that will cause the clock run method
        to stop.
        """
        self.__seconds = self.__default_time 
        self.set_string_var(self.__seconds)
        self.__exit.set()

    def __str__(self):
        """
        String representation of a clock object
        """
        return "{}:{}".format(self.__seconds//60,
                (str)(self.__seconds%60).zfill(2))

