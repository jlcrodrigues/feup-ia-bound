from view.pages.rules_view import RulesView

class RulesController:
    def __init__(self, gui):
        self.gui = gui
        text = "Rules"
        self.view = RulesView(gui, text)

    def play(self) -> bool:
        if not self.view.step(): return False

        return True




