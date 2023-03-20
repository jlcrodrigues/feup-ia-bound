from states.state import State
from controller.game_controller import GameController
from model.bot import Bot
from view.gui import GUI

from random import randint

class GameState(State):
    def __init__(self, gui: GUI, players: list):
        self.gui = gui
        self.controller = GameController(players[0], players[1], gui)

    def step(self):
        self.controller.play()
        from states.menu_state import MenuState
        return MenuState(self.gui)