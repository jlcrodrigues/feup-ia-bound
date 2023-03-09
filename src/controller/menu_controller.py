from view.menu_view import MenuView

class MenuController:
    def __init__(self, gui):
        self.gui = gui
        self.view = MenuView(gui)
        self.start = False
        self.mode = 1

    def play(self):
        self.view.step()
        self.mode = self.view.mode


