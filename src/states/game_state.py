from states.state import State
from controller.game_controller import GameController
from model.bot import Bot
from view.gui import GUI

from random import randint

class GameState(State):
    def __init__(self, gui, game_mode: int):
        self.gui = gui
        players = self.get_players(game_mode)
        self.controller = GameController(players[0], players[1], gui)
        pass

    def get_players(self, game_mode: int):
        """Determine who is playing according to the game mode:
            Player vs Player -> 1; Player vs CPU -> 2; CPU vs CPU -> 3
        """
        players = [None, None]
        if game_mode == 2:
            cpu = randint(0, 1)
            players[cpu] = Bot(cpu + 1, 0)
        elif game_mode == 3:
            players = [Bot(1, 0), Bot(2, 0)]

        return players


    def step(self):
        self.controller.play()
        from states.menu_state import MenuState
        return MenuState(self.gui)