from states.bot_menu_state import BotMenuState
from states.settings_menu_state import SettingsMenuState
from states.state import State
from states.game_state import GameState
from controller.menu_controller import MenuController
from view.gui import GUI

class MenuState(State):
    def __init__(self, gui):
        self.gui = gui
        self.controller = MenuController(gui)

    def step(self):
        self.controller.play()
        if self.controller.start:
            board_size = self.controller.board_size
            mode = self.controller.mode
            if mode > 1: return BotMenuState(self.gui, mode)
            return GameState(self.gui, [None, None],board_size)
        elif self.controller.settings:
            return SettingsMenuState(self.gui)