from model.board import Board, BLACK, WHITE

class Game:
    """
    A Bound Game instance. This model holds the logic to play the game.
    """
    def __init__(self):
        self.board = Board()
        self.player = BLACK
        self.winner = None
        self.over = False

    def next_player(self):
        """Switch players."""
        self.player = WHITE if self.player == BLACK else BLACK

    def move(self, source: tuple, dest: tuple):
        """Makes a move and updates the state of the game."""
        if source == None or dest == None:
            raise Exception("Trying to move null play.")
        self.board.move(self.player, source, dest)
        
        game_over, piece = self.board.did_bound(dest)
        
        if (game_over):
            self.over = True
            #print(f"Piece {piece} bound!")
            bounded = self.board.nodes[self.board.to_index(piece)].piece
            self.winner = WHITE if bounded == BLACK else BLACK 
            return

        self.next_player()

