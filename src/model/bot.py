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
        _, move = self.minimax(game, 2, True,self.evaluate_f1)
        return move
    
    def play_difficulty_2(self, game):
        """Play a move using the minimax algorithm."""
        _, move = self.minimax(game, 2, True,self.evaluate_f1)
        return move
    

    def minimax(self, game, depth, maximizing_player,evaluate_func,alpha=float('-inf'), beta=float('inf')):
        """Minimax algorithm with alpha-beta pruning."""
        if depth == 0 or game.over:
            # if game.over and depth > 0:
            #     print(f"game over depth: {depth}")
            return evaluate_func(game), None

        if maximizing_player:
            value = float('-inf')
            best_move = None
            # best_moves = []
            for move in game.board.get_moves(self.player):
                #print("maximizing")
                copy_game = copy.deepcopy(game)
                #print(f"player: {copy_game.player}, move: {move}")
                copy_game.move(move[0],move[1])
                new_value, _ = self.minimax(copy_game, depth - 1, False,evaluate_func,alpha,beta)
                # if new_value == value:
                #     best_moves.append((move,new_value))
                if new_value > value:
                    value = new_value
                    best_move = move 
                alpha = max(alpha, value)
                if beta <= alpha:
                    break  # beta cutoff
            # if depth == 6:
            #     print(f"max all moves: {game.board.get_moves(self.player)} \nlength: {len(game.board.get_moves(self.player))}")
            #     print(f"max best moves: {best_moves} \nlength: {len(best_moves)}")
            if best_move == None:
                best_move = choice(game.board.get_moves(self.player)) #random move            
            return value, best_move
        else:
            value = float('inf')
            best_move = None
            # best_moves = []
            for move in game.board.get_moves(self.opponent()):
                #print("minimizing")
                copy_game = copy.deepcopy(game)
                #print(f"player: {copy_game.player}, move: {move}")
                copy_game.move(move[0],move[1])
                new_value, _ = self.minimax(copy_game, depth - 1, True,evaluate_func,alpha,beta)
                # if new_value == value:
                #     best_moves.append((move,new_value))
                if new_value < value:
                    value = new_value
                    best_move = move
                beta = min(beta, value)
                if beta <= alpha:
                    break  # alpha cutoff
            # if depth == 6:
                # print(f"min all moves2: {game.board.get_moves(self.opponent())} \nlength: {len(game.board.get_moves(self.opponent()))}")
                # print(f"min best moves2: {best_moves} \nlength: {len(best_moves)}")           
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
        
    # def available_moves(self,game):
    #     return len(game.board.get_moves(self.player)) - len(game.board.get_moves(self.opponent()))

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
    
    def piece_coordination(self,game):
        result = 0
        board = game.board
        for node in board.pieces[self.opponent()]:
            for edge in board.nodes[board.to_index(node)].edges:
                for snd_edge in board.nodes[edge].edges:
                    if board.nodes[snd_edge].piece == self.player:
                        result += 1
                if board.nodes[edge].piece == self.player:
                    result += 3
        for node in board.pieces[self.player]:
            for edge in board.nodes[board.to_index(node)].edges:
                for snd_edge in board.nodes[edge].edges:
                    if board.nodes[snd_edge].piece == self.opponent():
                        result -= 1
                if board.nodes[edge].piece == self.opponent():
                    result -= 3
        return result                    
    
    def evaluate_f1(self,game):
       return self.game_is_over(game) + self.almost_bound(game) 

    def evaluate_f2(self,game):
        return self.game_is_over(game) + self.almost_bound(game) + self.piece_coordination(game)

    def opponent(self):
        """Returns the opponent's player color."""
        return BLACK if self.player == WHITE else WHITE