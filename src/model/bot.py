import copy
import math

from random import choice


class Bot:
    """
    Defines a bot player. The bot can be of different difficulty levels.
    """

    def __init__(self, player, difficulty):
        self.player = player
        if difficulty == 0:
            self.get_move = self.play_random
        if difficulty == 1:
            self.get_move = self.play_with_minimax

    def play(self, game):
        """Play a move. This function redirects the bot to the correct difficulty function."""
        return self.get_move(game.board)

    def play_random(self, game):
        """Play a random move."""
        return choice(game.board.get_moves(self.player))

    def mate_in_one(self, game):
        for move in game.board.get_moves(game.player):
            print(f"move: {move}")
            newgame = copy.deepcopy(game)
            newgame.move(move[0], move[1])
            if newgame.board.did_bound(move[1]):
                print(f"bound 1")
                return 1, move
        print("no bound possible")
        return 0, move

    def play_with_minimax(self, game):
        """Play a move using the minimax algorithm."""
        print("playing")
        _ , move = self.minimax(game, 0, -math.inf, math.inf, True, self.mate_in_one)
        return move


    def minimax(self, game, depth, alpha, beta, maximizing, evaluate_func):
        if depth == 0 or game.over:
            return evaluate_func(game)
        if maximizing:
            maxEval = -math.inf
            bestMove = None
            for move in game.board.get_moves(game.player):
                newgame = copy.deepcopy(game)
                newgame.move(move[0], move[1])
                evaluation, _ = self.minimax(
                    newgame, depth - 1, alpha, beta, False, evaluate_func)
                if evaluation > maxEval:
                    maxEval = evaluation
                    bestMove = move
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break
            return maxEval, bestMove
        else:
            minEval = math.inf
            bestMove = None
            for move in game.board.get_moves(game.player):
                newgame = copy.deepcopy(game)
                newgame.move(move[0], move[1])
                evaluation, _ = self.minimax(
                    newgame, depth - 1, alpha, beta, True, evaluate_func)
                if evaluation < minEval:
                    minEval = evaluation
                    bestMove = move
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break
            return minEval, bestMove
