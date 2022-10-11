#!/usr/bin/env python3

import tkinter as tk
import threading
import random

from tkinter.constants import DISABLED, NORMAL
from string import ascii_lowercase, ascii_uppercase
from words import *

NSEW = (tk.N, tk.S, tk.E, tk.W)
WINDOW_HEIGHT = 500
WINDOW_WIDTH = 600
TEXT_ENTRY_FONT = ("Times", 48)

class TextTwistUI:

    def __init__(self):
        self.root = tk.Tk()
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.create_content_pane(self.root)

        self.add_key_bindings_to_root()


    def add_key_bindings_to_root(self):
        """
        Bind keys for gameplay to root window.
        """
        self.root.bind_all("<space>", self.shuffle_letters)

        for letter in ascii_lowercase:
            self.root.bind_all(letter, self.process_typed_letter)

        self.root.bind_all("<BackSpace>", self.process_backspace)


    def create_content_pane(self, parent):
        """
        Create the main frame that will hold all content for the UI
        """
        content = tk.Frame(parent)
        top_pane = tk.Frame(content, relief="groove",
                borderwidth=2, width=WINDOW_WIDTH, height=WINDOW_HEIGHT/2)

        bottom_pane = tk.Frame(content, relief="groove",
                borderwidth=2, width=WINDOW_WIDTH, height=WINDOW_HEIGHT/2)
        content.grid(column=0, row=0, ipadx=5, ipady=5,
                sticky=NSEW)
        top_pane.grid(row=0, column=0, sticky=NSEW)
        bottom_pane.grid(row=1, column=0, sticky=NSEW)

        content.rowconfigure(0, weight=1)
        content.rowconfigure(1, weight=1)
        content.columnconfigure(0, weight=1)

        self.create_bottom_pane_frames(bottom_pane)


    def create_bottom_pane_frames(self, parent):
        """
        Create the two frames in the bottom pane that will hold the
        text entry area and the clock area
        """
        text_frame_weight = 2
        clock_frame_weight = 1
        text_frame_width = parent['width'] * text_frame_weight / \
            (text_frame_weight + clock_frame_weight)
        clock_frame_width = parent['width'] * clock_frame_weight / \
            (text_frame_weight + clock_frame_weight)
        self.create_text_frame(parent, text_frame_width, parent['height'])
        self.create_clock_frame(parent, clock_frame_width, parent['height'])

        parent.rowconfigure(0, weight=1)
        parent.columnconfigure(0, weight=text_frame_weight)
        parent.columnconfigure(1, weight=clock_frame_weight)


    def create_text_frame(self, parent, width, height):
        """
        Create the frame that will hold the text entry and letter
        display areas.
        """
        text_frame = tk.Frame(parent, relief="groove", borderwidth=2,
                width=width, height=height)
        text_frame.grid(row=0, column=0, sticky=NSEW)

        padding = {"padx":5, "pady":5}
        self.add_text_entry_frame(text_frame, text_frame['width'],
                text_frame['height']/2, padding)
        self.add_letter_display_frame(text_frame, text_frame['width'],
                text_frame['height']/2, padding)

        text_frame.rowconfigure(0, weight=1)
        text_frame.rowconfigure(1, weight=1)
        text_frame.columnconfigure(0, weight=1)


    def add_text_entry_frame(self, parent, width, height, padding):
        text_entry_frame = tk.Frame(parent, width=width, height=height)
        text_entry_frame.grid(row=0, column=0, sticky=NSEW, **padding)

        self.add_text_entry_boxes(text_entry_frame)


    def add_text_entry_boxes(self, parent):
        """
        Add boxes which will display characters that the user types.
        """
        self.entry_labels = []
        for i in range(6):
            label = tk.Label(parent, text="_",
                    font=TEXT_ENTRY_FONT, bg="white")
            label.grid(row=0, column=i)
            self.entry_labels.append(label)

        parent.rowconfigure(0, weight=1)
        parent.grid_propagate(False)
        for i in range(parent.grid_size()[0]):
            parent.columnconfigure(i, weight=1)


    def add_letter_display_frame(self, parent, width, height, padding):
        """
        Add the frame which will show the available letters for the puzzle.
        """
        letter_display_frame = tk.Frame(parent, width=width, height=height)
        letter_display_frame.grid(row=1, column=0, sticky=NSEW, **padding)

        self.add_letter_boxes(letter_display_frame)


    def add_letter_boxes(self, parent):
        """
        Add the individual labels that will hold each available letter
        for the puzzle.
        """
        self.letter_labels = []

        for i in range(6):
            label = tk.Label(parent, font=TEXT_ENTRY_FONT)
            label.grid(row=0, column=i)
            self.letter_labels.append(label)

        parent.rowconfigure(0, weight=1)
        parent.grid_propagate(False)
        for i in range(parent.grid_size()[0]):
            parent.columnconfigure(i, weight=1)


    def set_letters(self, letters=[" "]*6):
        """
        Set the letters in the letter display labels.
        """
        self.letters = letters
        random.shuffle(self.letters)
        for i, c in enumerate(self.letters):
            self.letter_labels[i].config(text=c)


    def shuffle_letters(self, *args):
        """
        Shuffle the puzzle letters in the UI.
        """
        random.shuffle(self.letter_labels)
        for i, label in enumerate(self.letter_labels):
            label.grid(row=0, column=i)


    def create_clock_frame(self, parent, width, height):
        """
        Create the frame that will hold the game clock and the buttons
        to start and reset the game.
        """
        self.clock_frame = tk.Frame(parent, relief="groove", borderwidth=2,
            width=width, height=height)
        self.clock_frame.grid(row=0, column=1, sticky=NSEW)

        self.clock_frame.rowconfigure(0, weight=3)
        self.clock_frame.rowconfigure(1, weight=1)
        self.clock_frame.rowconfigure(2, weight=1)
        self.clock_frame.columnconfigure(0, weight=1)

    
    def add_clock(self, clock, clock_run_callback, clock_reset_callback):
        self.add_clock_to_frame(self.clock_frame,
                clock, clock_run_callback, clock_reset_callback)


    def add_clock_to_frame(self, parent, clock, run_clock, reset_clock):
        """
        Add a clock to the parent frame.
        """
        self.clock_label = tk.Label(parent, textvariable=clock.get_string_var(),
                font=('bitstream charter', 36), anchor="center")
        self.clock_label.grid(row=0, column=0)

        self.add_clock_frame_buttons(parent, run_clock, reset_clock)


    def add_clock_frame_buttons(self, parent, run_clock, reset_clock):
        """
        Add start and reset buttons to the clock frame specified by
        'parent.'
        """
        self.start_btn = tk.Button(parent, text="Start",
                command=lambda : self.start_game(run_clock))
        self.start_btn.grid(row=1, column=0)
        self.reset_btn = tk.Button(parent, text="Reset",
            command=lambda : self.reset_game(reset_clock))
        self.reset_btn.grid(row=2, column=0)

    
    def process_typed_letter(self, event):
        """
        Update the letter display and text entry labels when a
        letter is typed.
        """
        typed_letter = event.char.upper()
        if typed_letter in ascii_uppercase:
            for letter_label in self.letter_labels:
                if typed_letter == letter_label['text']:
                    self.append_letter_to_text_entry(typed_letter)
                    letter_label['text'] = ' '
                    break


    def append_letter_to_text_entry(self, typed_letter):
        for entry_label in self.entry_labels:
            if entry_label['text'] == '_':
                entry_label['text'] = typed_letter
                break


    def process_backspace(self, event):
        """
        Find last non-empty letter entry. Move that letter from entry
        area to display area.
        """
        for entry_label in reversed(self.entry_labels):
            if entry_label['text'] != '_':
                self.move_letter_from_entry_to_display(entry_label)
                break


    def move_letter_from_entry_to_display(self, entry_label):
        """
        Find first available/empty letter display label, and move
        the text of 'entry_label' to the display.
        """
        for display_label in self.letter_labels:
            if display_label['text'] == ' ':
                display_label['text'] = entry_label['text']
                entry_label['text'] = '_'
                break


    def start_game(self, run_clock):
        self.start_btn['state'] = DISABLED
        self.set_letters(list(get_six_letter_word().upper()))
        run_clock()


    def reset_game(self, reset_clock):
        self.start_btn['state'] = NORMAL
        self.set_letters()
        reset_clock()


    def add_game_function_to_ui(self, name, func):
        self.functions[name] = func


    def start(self):
        self.root.mainloop()


if __name__ == '__main__':
    ui = TextTwistUI()
