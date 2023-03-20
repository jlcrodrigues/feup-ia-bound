from model.game import Game
from model.bot import Bot
from view.pages.game_view import GameView

from time import sleep

class GameController:
    """
    Controls the game flow. Connects view to the model.
    Can be executed without a view, so the bots are easier to test.
    Players can either be a Bot instance or None (for human players).
    """
    def __init__(self, player_1, player_2, gui=None):
        if (gui == None and (player_1 == None or player_2 == None)):
            raise ValueError("If no GUI is provided, both players must be bots.")
        self.game = Game()
        self.players = {}
        self.rounds = 0
        self.close = False

        self.player_1 = player_1
        self.player_2 = player_2
        self.player = self.player_1

        self.view = GameView(gui, self.game)

    def play(self):
        """Play out a full game."""
        while (not self.close):
            self.step()
        
        self.view.step()
        
        return self.game.winner

    def step(self):
        """Play one round of the game."""
        self.close = self.view.step()
        if (self.game.over): return
        if self.step_move():
            self.rounds += 1

    def step_move(self):
        """Execute a move given by the current player."""
        if self.player == None: 
            next_move = self.get_user_input()
        else:
            next_move = self.player.get_move(self.game)

        if next_move == None: return False

        self.game.move(next_move[0], next_move[1])

        if (self.game.over):
            print("Game ended, winner: ", str(self.game.winner), " , rounds: " , str(self.rounds))
            return True

        self.next_player()
        return True

    def next_player(self):
        """Switch players."""
        self.player = self.player_2 if self.player == self.player_1 else self.player_1 

    def get_current_player(self):
        return self.game.player

    def get_user_input(self):
        """Get user input from the view."""
        return self.view.get_user_input()