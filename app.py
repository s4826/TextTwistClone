from texttwistgame import TextTwistGame
from ui import TextTwistUI


if __name__ == "__main__":
    ui = TextTwistUI()
    game = TextTwistGame()

    ui.add_game_object_to_ui(game)
    ui.start_mainloop()
