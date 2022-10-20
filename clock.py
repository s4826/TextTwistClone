from threading import Event
from tkinter import StringVar

from time import sleep

class Clock():
    """
    Class to encapsulate a text twist game clock. Provides mechanisms
    for running the clock, resetting it, and notifying observers when
    notable events occur (i.e. clock reaches zero)
    """

    def __init__(self, default_time=120):
        """
        Initialize a clock with a StringVar (used by tkinter),
        a default time, an observers set, and an exit event.
        """
        self.string_var = StringVar()
        self.__default_time = default_time
        self.__seconds = default_time

        self.observers = set()

        self.__exit = Event()

        self.string_var.set(str(self))

    def _get_time(self):
        """
        Get current time on the clock in seconds
        """
        return self.__seconds

    def run(self):
        """
        Reset the clock to default time and start
        """
        self.reset()            # reset clock to starting state
        self.__exit.clear()     # clock exit event should be unset at start
        while True:
            # break out of loop if exit event is set while clock is running
            if self.__exit.is_set():
                self.__exit.clear()
                break
            self -= 1
            self.string_var.set(str(self))
            if self.__seconds == 0:
                self._notify_clock_reached_zero()
                break
            sleep(1)

    def _notify_clock_reached_zero(self):
        """
        Notify all observers that the clock reached zero
        """
        for observer_func in self.observers:
            observer_func()

    def set_to_zero(self):
        """
        Set the clock to zero
        """
        self.__seconds = 0
        self.__exit.set()
        self.string_var.set(str(self))
        self._notify_clock_reached_zero()

    def reset(self):
        """
        Reset the clock to the default time, and set the
        exit event that will cause the clock run method
        to stop.
        """
        self.__seconds = self.__default_time
        self.string_var.set(str(self))
        self.__exit.set()

    def __str__(self):
        """
        String representation of a clock object
        """
        return "{}:{}".format(self.__seconds//60,
                (str)(self.__seconds%60).zfill(2))

    def __isub__(self, arg: int):
        """
        Magic method for decrementing clock seconds
        """
        self.__seconds -= arg
        return self
