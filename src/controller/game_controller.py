from model.game import Game
from model.bot import Bot

class GameController:
    """
    Controls the game flow. Connects view to the model.
    Can be executed without a view, so the bots are easier to test.
    """
    def __init__(self, player_1, player_2, include_gui = True):
        self.game = Game()
        self.players = {}
        self.rounds = 0

        self.player_1 = player_1
        self.player_2 = player_2
        self.player = self.player_1

        if not include_gui:
            self.step_display = lambda : None
        else:
            self.step_display = self.display

    def play(self):
        """Play out a full game."""
        # display & fetch movement
        while (not self.game.over):
            self.step()

        return self.game.player

    def step(self):
        """Play one round of the game."""
        self.step_display()
        self.rounds += 1
        next_move = self.player.get_move(self.game.board)
        self.game.move(next_move[0], next_move[1])

        if (self.game.over):
            print("Game ended, winner: ", str(self.game.player), " , rounds: " , str(self.rounds))
            return

        self.next_player()

    def next_player(self):
        """Switch players."""
        self.player = self.player_2 if self.player == self.player_1 else self.player_1 

    def display(self):
        # TODO
        print('Displaying game state...')

    def get_current_player(self):
        return self.game.player