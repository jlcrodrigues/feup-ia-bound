import copy
import math

from random import choice

BLACK = 1
WHITE = 2

class Bot:
    """
    Defines a bot player. The bot can be of different difficulty levels.
    """

    def __init__(self, player, difficulty):
        self.player = player
        if difficulty == 0:
            self.get_move = self.play_random
        elif difficulty == 1:
            self.get_move = self.play_difficulty_1     

    def play(self, game):
        """Play a move. This function redirects the bot to the correct difficulty function."""
        return self.get_move(game.board)

    def play_random(self, game):
        """Play a random move."""
        return choice(game.board.get_moves(self.player))

    def play_difficulty_1(self, game):
        """Play a move using the minimax algorithm."""
        _, move = self.minimax(game, 6, True,self.eval_func_1)
        return move
    

    def minimax(self, game, depth, maximizing_player,evaluate_func,alpha=float('-inf'), beta=float('inf')):
        """Minimax algorithm with alpha-beta pruning."""
        if depth == 0 or game.over:
            if game.over and depth > 0:
                print(f"game over depth: {depth}")
                
            return evaluate_func(game), None

        if maximizing_player:
            value = float('-inf')
            best_move = None
            best_moves = []
            for move in game.board.get_moves(self.player):
                #print("maximizing")
                copy_game = copy.deepcopy(game)
                #print(f"player: {copy_game.player}, move: {move}")
                copy_game.move(move[0],move[1])
                new_value, _ = self.minimax(copy_game, depth - 1, False,evaluate_func,alpha,beta)
                if new_value == value:
                    best_moves.append((move,new_value))
                if new_value > value:
                    value = new_value
                    best_moves = [(move,new_value)]
                alpha = max(alpha, value)
                if beta <= alpha:
                    break  # beta cutoff
            if depth == 6:
                print(f"all moves: {game.board.get_moves(self.player)} \nlength: {len(game.board.get_moves(self.player))}")
                print(f"best moves: {best_moves} \nlength: {len(best_moves)}")
            best_move = choice(best_moves)[0]
            return value, best_move
        else:
            value = float('inf')
            best_move = None
            best_moves = []
            for move in game.board.get_moves(self.opponent()):
                #print("minimizing")
                copy_game = copy.deepcopy(game)
                #print(f"player: {copy_game.player}, move: {move}")
                copy_game.move(move[0],move[1])
                new_value, _ = self.minimax(copy_game, depth - 1, True,evaluate_func,alpha,beta)
                if new_value == value:
                    best_moves.append((move,new_value))
                if new_value < value:
                    value = new_value
                    best_moves = [(move,new_value)]
                beta = min(beta, value)
                if beta <= alpha:
                    break  # alpha cutoff
            if depth == 6:
                print(f"all moves: {game.board.get_moves(self.opponent())} \nlength: {len(game.board.get_moves(self.opponent()))}")
                print(f"best moves: {best_moves} \nlength: {len(best_moves)}")
            best_move = choice(best_moves)[0]
            
            
            return value, best_move

    def game_is_over(self, game):
        """Evaluation function that checks if the game is over."""
        if game.over:
            #print("game over")
            if game.winner == self.player:
                #print("win")
                return 1000
            else:
                #print("lost")
                return -1000
        else:
            return 0

    def eval_func_1(self,game):
        result = 0
        board = game.board
        for node in board.nodes:
            if node.piece == self.player:
                for edge in node.edges:
                    if board.nodes[edge].piece == 0:
                        result += 1
            elif node.piece == self.opponent():
                for edge in node.edges:
                    if board.nodes[edge].piece == 0:
                        result -= 1
        return result

    def opponent(self):
        """Returns the opponent's player color."""
        return BLACK if self.player == WHITE else WHITE