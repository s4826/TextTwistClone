import sys
import os
import unittest
import tkinter as tk

sys.path.insert(0, os.path.abspath('..'))

from clock import Clock

class TestClock(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        self.clock = Clock()

    def test_clock_default_time(self):
        self.assertEqual(self.clock.get_time(), 120)

    def test_get_time_string(self):
        self.assertEqual(self.clock.get_time_string(), "2:00")

    def test_add_observer(self):
        self.clock.add_observer(self)
        self.assertIsInstance(self.clock._Clock__observers.pop(),
                TestClock)

    def tearDown(self):
        self.root.destroy()


if __name__ == '__main__':
    unittest.main()
