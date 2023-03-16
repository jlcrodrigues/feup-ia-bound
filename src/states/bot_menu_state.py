from states.state import State
from controller.bot_menu_controller import BotMenuController
from view.gui import GUI

class BotMenuState(State):
    def __init__(self, gui: GUI, mode: int):
        self.gui = gui
        self.controller = BotMenuController(gui, mode)

    def step(self):
        if self.controller.play():
            from states.game_state import GameState
            return GameState(self.gui, self.controller.players)

        from states.menu_state import MenuState
        return MenuState(self.gui)