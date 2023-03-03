from model.game import Game
from model.bot import Bot
from view.game_view import GameView

from time import sleep

class GameController:
    """
    Controls the game flow. Connects view to the model.
    Can be executed without a view, so the bots are easier to test.
    """
    def __init__(self, player_1, player_2, gui=None):
        self.game = Game()
        self.players = {}
        self.rounds = 0

        self.player_1 = player_1
        self.player_2 = player_2
        self.player = self.player_1

        self.view = GameView(gui, self.game)

    def play(self):
        """Play out a full game."""
        while (not self.game.over):
            self.step()
             
        while (True): # TODO looping so the window doesn't close
            self.view.step()

        return self.game.player

    def step(self):
        """Play one round of the game."""
        self.view.step()
        if (self.game.over): return
        sleep(0.2)
        self.step_move()
        self.rounds += 1

    def step_move(self):
        """Execute a move given by the current player."""
        next_move = self.player.get_move(self.game.board)
        self.game.move(next_move[0], next_move[1])

        if (self.game.over):
            print("Game ended, winner: ", str(self.game.player), " , rounds: " , str(self.rounds))
            return

        self.next_player()

    def next_player(self):
        """Switch players."""
        self.player = self.player_2 if self.player == self.player_1 else self.player_1 

    def get_current_player(self):
        return self.game.player