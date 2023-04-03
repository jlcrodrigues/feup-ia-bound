from states.state import State
from controller.rules_controller import RulesController
from view.gui import GUI

class RulesState(State):
    def __init__(self, gui: GUI):
        self.gui = gui
        self.controller = RulesController(gui)

    def step(self):
        self.controller.play()
        
        from states.menu_state import MenuState
        return MenuState(self.gui)