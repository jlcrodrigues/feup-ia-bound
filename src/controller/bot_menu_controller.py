from model.bot import Bot
from view.bot_menu_view import BotMenuView
from random import randint

class BotMenuController:
    def __init__(self, gui, mode: int):
        self.gui = gui
        self.mode = mode
        text = "Choose your opponent" if mode == 2 else "Choose the first CPU"
        self.view = BotMenuView(gui, text)
        self.players = [None, None]

    def play(self) -> bool:
        """Get the bot difficulties and create the bots.
            For cpu vs cpu, the selection menu will run twice.

        Returns:
            bool: False if user exited to menu and True if the selection was OK.
        """
        if not self.view.step(): return False
        selection = self.view.selection
        pos = 0 if self.mode > 2 else randint(0, 1)
        self.players[pos] = Bot(pos + 1, selection[0])

        if self.mode > 2:
            self.view = BotMenuView(self.gui, "Choose the second CPU")
            if not self.view.step():
                return False
            selection = self.view.selection
            self.players[1] = Bot(2, selection[0])

        return True




