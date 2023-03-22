from states.bot_menu_state import BotMenuState
from states.state import State
from states.game_state import GameState
from controller.menu_controller import MenuController
from model.player import Player
from view.gui import GUI

class MenuState(State):
    def __init__(self, gui):
        self.gui = gui
        self.controller = MenuController(gui)

    def step(self):
        self.controller.play()
        mode = self.controller.mode
        if mode > 1: return BotMenuState(self.gui, mode)
        return GameState(self.gui, [Player(1), Player(2)])