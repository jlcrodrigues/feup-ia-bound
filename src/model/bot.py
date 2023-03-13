import copy
import math
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
        if difficulty == 1:
            self.get_move = self.play_with_minimax

    def play(self, game):
        """Play a move. This function redirects the bot to the correct difficulty function."""
        return self.get_move(game.board)

    def play_random(self, game):
        """Play a random move."""
        return choice(game.board.get_moves(self.player))
    
    def mate_in_one(self, game):
        for move in game.board.get_moves(self.player):
            if game.board.did_bound(move[1]):
                print(f"bound 1")
                return 1
        print(f"bound 0")
        return 0
            
    def play_with_minimax(self, game):
        """Play a move using the minimax algorithm."""
        return self.minimax(game, 1, -math.inf,math.inf,True,self.mate_in_one)
    
    
    def minimax(self,game,depth,alpha,beta,maximizing,evaluate_func):
        print(f"depth {depth}")
        if depth == 0 or game.over:
            return evaluate_func(game)
        if maximizing:
            maxEval = -math.inf
            for move in game.board.get_moves(game.player):
                print(f"move {move}")
                print(f"player {game.player}")
                newgame = copy.deepcopy(game)
                newgame.move(move[0],move[1])
                evaluation = self.minimax(newgame,depth-1,alpha,beta,False,evaluate_func)
                maxEval = max(maxEval, evaluation)
                print(f"max {maxEval}")
                print(f"eval {evaluation}")
                print(f"alpha1 {alpha}")
                alpha = max(alpha, evaluation)
                print(f"beta1 {beta}")
                if beta <= alpha: 
                    print(f"break1")
                    break
            return maxEval
        else:
            minEval = math.inf
            
            for move in game.board.get_moves(game.player):
                print(f"move2 {move}")
                print(f"player2 {game.player}")
                game.move(move[0],move[1])
                evaluation = self.minimax(game,depth-1,alpha,beta,True,evaluate_func)
                print(f"min {minEval}")
                print(f"eval2 {evaluation}")
                minEval = min(minEval, evaluation)
                print(f"beta2 {beta}")
                beta = min(beta, evaluation)
                print(f"alpha2 {alpha}")
                if beta <= alpha: 
                    print(f"break2")
                    break
            return minEval



