from states.state import State
from controller.game_controller import GameController
from model.bot import Bot
from view.gui import GUI

class GameState(State):
    def __init__(self, gui):
        self.controller = GameController(Bot(1, 0), Bot(2, 0), gui)
        pass

    def step(self):
        winner = self.controller.play()
        return None