import sys
import os
import unittest
import tkinter as tk
import time

from threading import Thread
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.abspath('..'))

from clock import Clock
from texttwistgame import TextTwistGame

class TestClock(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        self.clock = Clock()

    def test_clock_default_time(self):
        self.assertEqual(self.clock._get_time(), 120)

    def test_repr(self):
        self.assertEqual(str(self.clock), "2:00")

    def test_observer(self):
        mock = MagicMock(TextTwistGame)

        self.clock.observers.add(mock.notify_clock_reached_zero)
        self.clock._notify_clock_reached_zero()
        mock.notify_clock_reached_zero.assert_called_once()

    def test_set_to_zero(self):
        self.clock = Clock()
        self.clock.set_to_zero()
        
        self.assertEqual(self.clock.string_var.get(), "0:00")

    def test_reset(self):
        self.clock = Clock(1)
        start_string = str(self.clock)
        self.clock.run()

        self.assertNotEqual(start_string, str(self.clock))

        self.clock.reset()

        self.assertEqual(start_string, str(self.clock))

    def test_isub(self):
        self.clock = Clock(10)
        self.clock -= 1
        self.assertEqual(self.clock._get_time(), 9)

    def tearDown(self):
        self.root.destroy()


if __name__ == '__main__':
    unittest.main()
