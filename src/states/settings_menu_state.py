from states.state import State
from controller.settings_menu_controller import SettingsMenuController
from view.gui import GUI

class SettingsMenuState(State):
    def __init__(self, gui: GUI):
        self.gui = gui
        self.controller = SettingsMenuController(gui)

    def step(self):
        self.controller.play()
        
        from states.menu_state import MenuState
        return MenuState(self.gui)