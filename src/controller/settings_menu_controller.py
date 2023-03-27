from model.bot import Bot
from view.pages.settings_menu_view import SettingsMenuView
from random import randint

class SettingsMenuController:
    def __init__(self, gui):
        self.gui = gui
        text = "Settings"
        self.view = SettingsMenuView(gui, text)

    def play(self) -> bool:
        if not self.view.step(): return False

        return True




