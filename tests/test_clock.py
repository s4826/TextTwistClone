import sys
import os
import unittest
import tkinter as tk

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

    def test_add_observer(self):
        mock = MagicMock(TextTwistGame)

        self.clock.add_observer(mock.notify_clock_reached_zero)
        self.clock._notify_clock_reached_zero()
        mock.notify_clock_reached_zero.assert_called_once()

    @patch.object(Clock, "_notify_clock_reached_zero")
    def test_run_clock_to_zero(self, func):
        self.clock = Clock(1)
        self.clock.run()

        self.assertTrue(func.called)

    def tearDown(self):
        self.root.destroy()


if __name__ == '__main__':
    unittest.main()
