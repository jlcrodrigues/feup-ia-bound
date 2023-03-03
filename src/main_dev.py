"""
This file can be used to better test the AI without the GUI.
"""

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

from model.bot import Bot
from controller.game_controller import GameController

def main_dev():
    game = GameController(Bot(1, 0), Bot(2, 0))

    game.play()

main_dev()