from states.state import State
from controller.about_controller import AboutController
from view.gui import GUI

class AboutState(State):
    def __init__(self, gui: GUI):
        self.gui = gui
        self.controller = AboutController(gui)

    def step(self):
        self.controller.play()
        
        from states.menu_state import MenuState
        return MenuState(self.gui)