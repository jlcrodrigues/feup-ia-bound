from view.pages.about_view import AboutView

class AboutController:
    def __init__(self, gui):
        self.gui = gui
        text = "About"
        self.view = AboutView(gui, text)

    def play(self) -> bool:
        if not self.view.step(): return False

        return True




