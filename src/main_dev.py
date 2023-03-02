"""
This file can be used to better test the AI without the GUI.
"""

from model.bot import Bot
from controller.game_controller import GameController

def main():
    game = GameController(Bot(1, 0), Bot(2, 0), False)

    game.play()

if __name__ == "__main__":
    main()