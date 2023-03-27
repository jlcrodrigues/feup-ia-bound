from model.bot import Bot
from model.player import Player
from view.pages.bot_menu_view import BotMenuView
from random import randint

class BotMenuController:
    def __init__(self, gui, mode: int):
        self.gui = gui
        self.mode = mode
        text = "Choose your opponent" if mode == 2 else "Choose the first CPU"
        self.view = BotMenuView(gui, text)
        self.players = [Player(1), Player(2)]

    def play(self) -> bool:
        """Get the bot difficulties and create the bots.
            For cpu vs cpu, the selection menu will run twice.

        Returns:
            bool: False if user exited to menu and True if the selection was OK.
        """
        if not self.view.step(): return False
        selection = self.view.selection
        pos = 0 if self.mode > 2 else randint(0, 1)
        bot1 = Bot(pos + 1, selection)
        if selection == "Martim":
            bot1.bot_settings.minimax_depth = self.view.minimax_depth
            bot1.bot_settings.minimax_evaluate = self.view.minimax_evaluate
        elif selection == "Luís":
            bot1.bot_settings.montecarlo_exploration = self.view.montecarlo_exploration
            bot1.bot_settings.montecarlo_simulations = self.view.montecarlo_simulations
        self.players[pos] = bot1

        if self.mode > 2:
            self.view = BotMenuView(self.gui, "Choose the second CPU")
            if not self.view.step():
                return False
            selection = self.view.selection
            bot2 = Bot(2, selection)
            if selection == "Martim":
                bot2.bot_settings.minimax_depth = self.view.minimax_depth
                bot2.bot_settings.minimax_evaluate = self.view.minimax_evaluate
            elif selection == "Luís":
                bot2.bot_settings.montecarlo_exploration = self.view.montecarlo_exploration
                bot2.bot_settings.montecarlo_simulations = self.view.montecarlo_simulations
            self.players[1] = bot2

        return True




