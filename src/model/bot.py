import copy
import math
import numpy as np
from collections import defaultdict

from model.player import *
from model.bot_settings import BotSettings

from random import choice, uniform

BOTS = {
    "Tiago": 0,
    "Martim": 1,
    "Luís": 2
}

class Bot(Player):
    """
    Defines a bot player. The bot can be of different difficulty levels.
    """

    def __init__(self, player: int, bot_name : str):
        super().__init__(player)
        self.is_bot = True
        self.name = bot_name
        self.bot_settings = BotSettings()
        difficulty = BOTS[bot_name]

        if (difficulty > 2): raise ValueError(f"That bot difficulty does not exist: {difficulty}")
        if difficulty == 0:
            self.get_move = self.play_random
        elif difficulty == 1:
            self.get_move = self.play_difficulty_1
        elif difficulty == 2:
            self.get_move = self.play_difficulty_2 

    def play(self, game):
        """Play a move. This function redirects the bot to the correct difficulty function."""
        return self.get_move(game.board)

    def play_random(self, game):
        """Play a random move."""
        return choice(game.board.get_moves(self.player))

    def play_difficulty_1(self, game):
        """Play a move using the minimax algorithm."""
        _, move = self.minimax(game,self.bot_settings.minimax_depth,True,self.get_evaluate_func())
        return move
    
    def play_difficulty_2(self, game):
        """Play a move using the montecarlo algorithm."""
        move = self.monte_carlo(game,self)
        return move

    def get_evaluate_func(self):
        if self.bot_settings.minimax_evaluate == 1:
            return self.evaluate_f1
        elif self.bot_settings.minimax_evaluate == 2:
            return self.evaluate_f2
        elif self.bot_settings.minimax_evaluate == 3:
            return self.evaluate_f3
    
    def minimax(self, game, depth, maximizing_player,evaluate_func,alpha=float('-inf'), beta=float('inf')):
        """Minimax algorithm with alpha-beta pruning."""
        if depth == 0 or game.over:
            return evaluate_func(game), None

        if maximizing_player:
            value = float('-inf')
            best_move = None
            for move in game.board.get_moves(self.player):
                copy_game = copy.deepcopy(game)
                copy_game.move(move[0],move[1])
                new_value, _ = self.minimax(copy_game, depth - 1, False,evaluate_func,alpha,beta)
                if new_value > value:
                    value = new_value
                    best_move = move 
                alpha = max(alpha, value)
                if beta <= alpha:
                    break  # beta cutoff
            if best_move == None:
                best_move = choice(game.board.get_moves(self.player)) #random move            
            return value, best_move
        else:
            value = float('inf')
            best_move = None
            for move in game.board.get_moves(self.opponent()):
                copy_game = copy.deepcopy(game)
                copy_game.move(move[0],move[1])
                new_value, _ = self.minimax(copy_game, depth - 1, True,evaluate_func,alpha,beta)
                if new_value < value:
                    value = new_value
                    best_move = move
                beta = min(beta, value)
                if beta <= alpha:
                    break  # alpha cutoff         
            if best_move == None:
                best_move = choice(game.board.get_moves(self.player)) #random move
            return value, best_move
    
    """Evaluation function that checks if the game is over."""
    def game_is_over(self, game):
        if game.over:
            if game.winner == self.player:
                return 1000
            else:
                return -1000
        else:
            return 0

    def almost_bound(self,game):
        result = 0
        board = game.board
        for node in board.nodes:
            spaces = 0
            if node.piece == self.player:
                for edge in node.edges:
                    if board.nodes[edge].piece == 0:
                        spaces += 1
                if spaces == 1:
                    result -= 10
            elif node.piece == self.opponent():
                for edge in node.edges:
                    if board.nodes[edge].piece == 0:
                        spaces += 1
                if spaces == 1:
                    result += 10
        return result
    
    def evaluate_f1(self,game):
       return self.almost_bound(game) + uniform(0,0.01)

    def evaluate_f2(self,game):
        return self.game_is_over(game) + uniform(0,0.01)

    def evaluate_f3(self,game):
        return self.evaluate_f1(game) + self.evaluate_f2(game)
    
    def opponent(self):
        """Returns the opponent's player color."""
        return BLACK if self.player == WHITE else WHITE
    

    def monte_carlo(self, game, bot):
        """Play a move using Monte Carlo Tree Search."""
        root = TreeNode(game, None, None, bot)
        return root.best_move()
    
class TreeNode:
    def __init__(self, game, move, parent, bot):
        self.game = game
        self.move = move
        self.parent = parent
        self.bot = bot
        self.children = []
        self.visits = 0
        self._results = defaultdict(int)
        self._results[BLACK] = 0
        self._results[WHITE] = 0
        self.untried_moves = self.untried_moves()
    
    def untried_moves(self):
        self._untried_moves = self.game.board.get_moves(self.game.player)
        return self._untried_moves
    
    def q(self):
        """Return the action value (quality) of the node."""
        wins = self._results[self.bot.player]
        loses = self._results[self.bot.opponent()]
        return wins - loses
    
    def n(self):
        """Return the number of visits of the node."""
        return self.visits

    
    def expand(self):
        """Expand the tree by adding a child node for each untried move."""
        move = choice(self.untried_moves)
        copy_game = copy.deepcopy(self.game)
        copy_game.move(move[0], move[1])
        child = TreeNode(copy_game, move, self, self.bot)
        self.children.append(child)
        self.untried_moves.remove(move)
        return child
    
    def is_terminal(self):
        """Return True if the node is a terminal node."""
        return self.game.over
    
    def rollout(self):
        """Perform a random rollout from the current node."""
        copy_game = copy.deepcopy(self.game)
        while not copy_game.over:
            copy_game.move(*choice(copy_game.board.get_moves(copy_game.player)))
        return copy_game.winner

    def backpropagate(self, winner):
        self.visits += 1
        self._results[winner] += 1
        if self.parent:
            self.parent.backpropagate(winner)
            
    def is_full_expanded(self):
        """Return True if the node has been fully expanded."""
        return len(self.untried_moves) == 0
    
    def best_child(self, c_param):
        """Return the child with the highest UCB score."""
        choices_weights = [(c.q() / (c.n())) + c_param * np.sqrt(np.log(self.n()) / (c.n())) for c in self.children]
        return self.children[np.argmax(choices_weights)]
    
    def _tree_policy(self):
        """Return the best child using UCB1."""
        current = self
        while not current.is_terminal():
            if not current.is_full_expanded():
                return current.expand()
            else:
                current = current.best_child(self.bot.bot_settings.montecarlo_exploration)
        return current
    
    def _tree_to_string(self, indent):
        s = self.indent_string(indent) + str(self.move) + " " + str(self.q()) + " " + str(self.n())
        for c in self.children:
            s += c._tree_to_string(indent+1)
        return s
    
    def indent_string(self, indent):
        s = "\n"
        for i in range(1, indent+1):
            s += "| "
        return s
    
    def best_move(self):
        """Return the best move"""
        simulation_no = self.bot.bot_settings.montecarlo_simulations
        
        for i in range(simulation_no):
            leaf = self._tree_policy()
            winner = leaf.rollout()
            leaf.backpropagate(winner)

        return self.best_child(self.bot.bot_settings.montecarlo_exploration).move