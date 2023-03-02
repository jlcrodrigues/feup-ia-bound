from model.board import Board

from random import choice

class Bot:
    def __init__(self, player, difficulty):
        self.player = player
        if difficulty == 0:
            self.get_move = self.play_random

    def play(self, board):
        return self.get_move(board)

    def play_random(self, board):
        return choice(board.get_moves(self.player))


