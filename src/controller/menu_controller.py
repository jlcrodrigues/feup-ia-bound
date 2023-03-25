from view.pages.menu_view import MenuView

class MenuController:
    def __init__(self, gui):
        self.gui = gui
        self.view = MenuView(gui)
        self.start = False
        self.mode = 1
        self.board_size = 1

    def play(self):
        """Execute the menu until Play button is clicked. Determine game mode."""
        self.view.step()
        self.mode = self.view.mode
        self.board_size = self.view.board_size


