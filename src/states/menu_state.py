from states.state import State
from states.game_state import GameState
from controller.menu_controller import MenuController
from view.gui import GUI

class MenuState(State):
    def __init__(self, gui):
        self.gui = gui
        self.controller = MenuController(gui)
        pass

    def step(self):
        self.controller.play()
        mode = self.controller.mode
        return GameState(self.gui, mode)