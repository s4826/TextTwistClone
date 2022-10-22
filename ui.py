#!/usr/bin/env python3

import tkinter as tk
import threading
import random

from tkinter.constants import DISABLED, NORMAL
from string import ascii_lowercase, ascii_uppercase
from texttwistgame import INSTRUCTIONS

NSEW = (tk.N, tk.S, tk.E, tk.W)
WINDOW_HEIGHT = 500
WINDOW_WIDTH = 600
FONT = "Courier"
INSTRUCTIONS_FONT = (FONT, 16)
TEXT_ENTRY_FONT = (FONT, 48)
SOLUTION_WORD_FONT = (FONT, 24)
SOLUTION_GRID_HEIGHT = 7
MIN_SOLUTION_GRID_HEIGHT = 4
GAME_STATUS_FONT = (FONT, 24)

PUZZLE_WORD_LENGTH = 6

ON = 1
OFF = 0

class TextTwistUI:
    """
    Main game window/ui class

    Handles generation of UI components such as buttons and labels

    Handles UI updates based on user input (i.e. typing letters and words),
    and game events (i.e. correct word entered, current level passed,
    clock stopped)
    """

    def __init__(self):
        """
        Initialize tk root window and add the key bindings
        for gameplay.
        """
        self.__root = tk.Tk()
        self.__root.columnconfigure(0, weight=1)
        self.__root.rowconfigure(0, weight=1)
        self.create_content_pane(self.__root)

        self.create_key_bindings_dictionary()


    def create_key_bindings_dictionary(self):
        """
        Bind keys for gameplay to root window.
        """
        self.bindings = {}

        self.bindings["<space>"] = self.shuffle_letters

        for letter in ascii_lowercase:
            self.bindings[letter] = self.process_typed_letter

        self.bindings["<BackSpace>"] = self.process_backspace

        self.bindings["<Return>"] = self.validate_word

    
    def toggle_root_key_bindings(self, action=OFF):
        """
        Toggle all key bindings for the root window.
        """
        if action == ON:
            for event, function in self.bindings.items():
                self.__root.bind_all(event, function)
        elif action == OFF:
            for event in self.bindings:
                self.__root.unbind_all(event)


    def create_content_pane(self, parent):
        """
        Create the main frame that will hold all content for the UI.
        Create the top and bottom panes, which will provide logical
        separation between the solution and text entry (typing) areas
        """
        content = tk.Frame(parent)
        content.grid(column=0, row=0, ipadx=5, ipady=5,
                sticky=NSEW)

        pane_creation_kwargs = {
            "relief": "groove",
            "borderwidth": 2,
            "width": WINDOW_WIDTH,
            "height": WINDOW_HEIGHT/2
        }
        self.top_pane = tk.Frame(content, **pane_creation_kwargs)
        self.top_pane.grid(row=0, column=0, sticky=NSEW)
        self.bottom_pane = tk.Frame(content, **pane_creation_kwargs)
        self.bottom_pane.grid(row=1, column=0, sticky=NSEW)

        content.rowconfigure(0, weight=1)
        content.rowconfigure(1, weight=1)
        content.columnconfigure(0, weight=1)

        self.add_instruction_message()
        self.create_bottom_pane_frames(self.bottom_pane)


    def add_instruction_message(self):
        """
        Create the instructions message that will be displayed
        on startup and game reset.
        """
        self.instruction_message = tk.Message(self.top_pane,
                text=INSTRUCTIONS, font=INSTRUCTIONS_FONT, aspect=175)
        self.instruction_message.grid(row=0, column=0, sticky=NSEW)
        self.top_pane.rowconfigure(0, weight=1)
        self.top_pane.columnconfigure(0, weight=1)

       
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

        text_frame_child_args = (text_frame, text_frame['width'],
                text_frame['height']/3)
        self.add_text_entry_frame(*text_frame_child_args, padding)
        self.add_letter_display_frame(*text_frame_child_args, padding)
        self.add_game_status_frame(*text_frame_child_args)

        text_frame.rowconfigure(0, weight=1) # text entry area
        text_frame.rowconfigure(1, weight=1) # letter display area
        text_frame.rowconfigure(2, weight=1) # game status area
        text_frame.columnconfigure(0, weight=1)


    def add_text_entry_frame(self, parent, width, height, padding):
        """
        Add the frame to hold all text entry labels.
        """
        text_entry_frame = tk.Frame(parent, width=width, height=height)
        text_entry_frame.grid(row=0, column=0, sticky=NSEW, **padding)

        self.add_text_entry_labels(text_entry_frame)


    def add_text_entry_labels(self, parent):
        """
        Add boxes which will display characters that the user types.
        """
        self.entry_labels = []
        for i in range(PUZZLE_WORD_LENGTH):
            label = tk.Label(parent, font=TEXT_ENTRY_FONT, bg="white")
            label.grid(row=0, column=i)
            self.entry_labels.append(label)

        self.reset_entry_label_text()

        parent.rowconfigure(0, weight=1)
        parent.grid_propagate(False)
        for i in range(parent.grid_size()[0]):
            parent.columnconfigure(i, weight=1)


    def reset_entry_label_text(self, text="_"):
        """
        Reset all entry labels with default character, underscore.
        """
        for entry_label in self.entry_labels:
            entry_label['text'] = text


    def add_letter_display_frame(self, parent, width, height, padding):
        """
        Add the frame which will show the available letters for the puzzle.
        """
        letter_display_frame = tk.Frame(parent, width=width, height=height)
        letter_display_frame.grid(row=1, column=0, sticky=NSEW, **padding)

        self.add_letter_labels(letter_display_frame)


    def add_letter_labels(self, parent):
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


    def add_game_status_frame(self, parent, width, height):
        """
        Add frame that will hold the level status and score labels.
        """
        game_status_frame = tk.Frame(parent,
                width=width, height=height)
        game_status_frame.grid(row=2, column=0, sticky=NSEW)
        
        self.add_game_status_labels(game_status_frame)

        
    def add_game_status_labels(self, parent):
        """
        Add level status and score labels to game status frame.
        """
        self.level_status_label = tk.Label(parent,
                font=GAME_STATUS_FONT)
        self.level_status_label.grid(row=0, column=0, sticky=NSEW)
        self.score_label = tk.Label(parent,
                font=GAME_STATUS_FONT)
        self.score_label.grid(row=0, column=1, sticky=NSEW)

        parent.rowconfigure(0, weight=1)
        parent.columnconfigure(0, weight=2)
        parent.columnconfigure(1, weight=1)

    
    def clear_game_status_labels(self):
        """
        Set level status and score labels to blanks.
        """
        self.score_label['text'] = ""
        self.level_status_label['text'] = ""


    def clear_entry_and_display_letters(self):
        """
        Reset the text entry and letter display areas to all blanks.
        """
        self.reset_entry_label_text() 
        self.set_display_letters()


    def reset_entry_and_display_letters(self):
        """
        Move all letters from text entry area to display area,
        leaving text entry area blank.
        """
        self.reset_entry_label_text()
        self.set_display_letters(self.game.get_letters())


    def set_display_letters(self, letters=[" "]*6):
        """
        Set the letters in the letter display labels.
        """
        self.letters = letters
        random.shuffle(self.letters)
        for i, c in enumerate(self.letters):
            self.letter_labels[i].config(text=c)


    def set_solution_word_labels(self):
        """
        Populate top pane with empty text labels corresponding to each
        word in the solution set.
        """
        parent = self.top_pane
        self.solution_labels = []
        wordlist = self.game.get_wordlist()

        grid_width = set_grid_width(len(wordlist))
        grid_height = (len(wordlist) + grid_width - 1) // grid_width

        for i, word in enumerate(sorted(wordlist, key=len)):
            label = tk.Label(parent, font=SOLUTION_WORD_FONT,
                text="_"*len(word), bg="white")
            label.grid(row=(i%grid_height), column=(i//grid_height),
                    padx=3, pady=3)
            self.solution_labels.append(label)

        grid_dims = parent.grid_size()

        for j in range(grid_dims[0]):
            if 0 <= j < grid_width:
                parent.columnconfigure(j, weight=1)
            else:
                parent.columnconfigure(j, weight=0)
        for i in range(grid_dims[1]):
            if 0 <= i < grid_height:
                parent.rowconfigure(i, weight=1)
            else:
                parent.rowconfigure(i, weight=0)


    def clear_solution_word_labels(self):
        """
        Clear all labels from the top pane. Used to reset the state
        and appearance of the solution/entered word area to empty.
        """
        for widget in self.top_pane.winfo_children():
            widget.destroy()


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

    
    def add_clock(self, clock):
        """
        Add a clock instance to the ui.
        """
        self.add_clock_to_frame(self.clock_frame, clock)


    def add_clock_to_frame(self, parent, clock):
        """
        Add a clock to the parent frame.
        """
        self.clock_label = tk.Label(parent, textvariable=clock.string_var,
                font=('bitstream charter', 36), anchor="center")
        self.clock_label.grid(row=0, column=0)

        self.add_clock_frame_buttons(parent)


    def add_clock_frame_buttons(self, parent):
        """
        Add start and reset buttons to the clock frame specified by
        'parent.'
        """
        self.start_btn = tk.Button(parent, text="Start",
                command=self.start_game,
                takefocus=0)
        self.start_btn.grid(row=1, column=0)
        self.reset_btn = tk.Button(parent, text="Reset",
                command=self.reset_game,
                takefocus=0)
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
        """
        Helper method for processing typed letters. Find first
        empty/available label in the text entry area, and populate
        it with 'typed_letter.'
        """
        for entry_label in self.entry_labels:
            if entry_label['text'] == '_':
                entry_label['text'] = typed_letter
                break


    def validate_word(self, event):
        """
        Validate a typed word and update the ui accordingly.

        Once the word is confirmed valid, entry letters must be
        returned to the letter display area, and the entered word
        should be added to the solution area.
        """
        word = "".join(label['text'] for label in self.entry_labels if
                label['text'] != "_")
        if self.game.word_entry_is_valid(word):
            self.add_word_to_solution_area(word)
            self.reset_entry_and_display_letters()
            self.update_game_status()


    def add_word_to_solution_area(self, word, color="black"):
        """
        Populate the first empty/available solution area label
        with 'word'
        """
        for solution_label in self.solution_labels:
            if "_" in solution_label['text'] and \
                len(solution_label['text']) == len(word):
                solution_label['text'] = word
                solution_label['fg'] = color
                break


    def update_game_status(self):
        """
        Update the game status frame with any score increases
        and level status changes (i.e. level passed)
        """
        self.update_score_label()
        self.update_level_status_label()


    def update_score_label(self):
        """
        Update the score in the ui from the current score value
        in the game instance.
        """
        score = self.game.get_score()
        self.score_label['text'] = f"Score: {score}"


    def update_level_status_label(self):
        """
        Update level status in ui
        """
        if self.game.level_passed():
            self.level_status_label['text'] = "Level Passed!"
            self.start_btn['state'] = NORMAL
        else:
            self.level_status_label['text'] = ""
        

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
        Helper method for processing <BackSpace>. Find first
        available/empty letter display label, and move
        the text of 'entry_label' to that letter display label.
        """
        for display_label in self.letter_labels:
            if display_label['text'] == ' ':
                display_label['text'] = entry_label['text']
                entry_label['text'] = '_'
                break


    def display_missing_words(self):
        """
        Populate remaining solution area labels with words that
        haven't been entered yet.
        """
        missing_words = self.game.get_missing_solution_words()
        for word in sorted(missing_words, key=len):
            self.add_word_to_solution_area(word, color="red")


    def add_game_object_to_ui(self, game):
        """
        Pass an instance of TextTwistGame to the UI class. Game logic
        and events can be processed via the TextTwistGame object.
        """
        self.game = game
        self.add_clock(game.clock)
        self.game.add_ui_callback(
                "process_clock_reached_zero",
                self.process_clock_reached_zero)


    def process_clock_reached_zero(self):
        """
        Update the ui to display all missing words when the
        clock reaches zero.
        """
        self.display_missing_words()
        self.reset_entry_and_display_letters()
        self.toggle_root_key_bindings(OFF)
       
        # set next level available via start button
        if self.game.level_passed():
            self.start_btn['state'] = NORMAL


    def start_game(self):
        """
        Populate all necessary ui areas to start the game.
        """
        self.start_btn['state'] = DISABLED
        self.toggle_root_key_bindings(ON)

        self.game.start_game()
        self.set_display_letters(self.game.get_letters())
        self.clear_solution_word_labels()
        self.set_solution_word_labels()
        self.update_game_status()


    def reset_game(self):
        """
        Clear all ui areas and reset game state.
        """
        self.start_btn['state'] = NORMAL
        self.game.reset_game()
        self.clear_entry_and_display_letters()
        self.clear_solution_word_labels()
        self.clear_game_status_labels()
        
        self.add_instruction_message()


    def start_mainloop(self):
        """
        tkinter main event loop
        """
        self.__root.mainloop()


def set_grid_width(num_words):
    """
    Helper function to set width of a grid of words
    """
    width = (num_words + SOLUTION_GRID_HEIGHT - 1) // SOLUTION_GRID_HEIGHT
    return max(width, MIN_SOLUTION_GRID_HEIGHT)

