from states.state import State
from controller.game_controller import GameController

class GameState(State):
    def __init__(self):
        self.controller = GameController()
        pass

    def step(self):
        print("step")
        return None