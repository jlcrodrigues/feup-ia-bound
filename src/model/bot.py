from model.board import Board

from random import choice

class Bot:
    """
    Defines a bot player. The bot can be of different difficulty levels.
    """
    def __init__(self, player, difficulty):
        self.player = player
        if difficulty == 0:
            self.get_move = self.play_random

    def play(self, board):
        """Play a move. This function redirects the bot to the correct difficulty function."""
        return self.get_move(board)

    def play_random(self, board):
        """Play a random move."""
        return choice(board.get_moves(self.player))


