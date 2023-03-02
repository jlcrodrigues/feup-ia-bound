from states.state import State
from controller.game_controller import GameController
from model.bot import Bot

class GameState(State):
    def __init__(self):
        self.controller = GameController(Bot(1, 0), Bot(2, 0))
        pass

    def step(self):
        winner = self.controller.play()
        return None