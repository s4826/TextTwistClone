import threading
from texttwistgame import TextTwistGame
from ui import TextTwistUI


def handle_thread_exceptions(*args):
    """
    Consume any exceptions from spawned threads

    The game only spawns a single clock thread. Exiting the program
    while this clock thread is running raises a runtime exception,
    which we don't need to handle (in the current iteration
    of this program).
    """
    pass


if __name__ == "__main__":
    """
    Main application start location
    """

    # redefine hook for thread exceptions
    threading.excepthook = handle_thread_exceptions

    ui = TextTwistUI()
    game = TextTwistGame()

    ui.add_game_object_to_ui(game)
    ui.start_mainloop()
