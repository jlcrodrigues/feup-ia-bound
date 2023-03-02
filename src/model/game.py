from src.model.board import Board, BLACK, WHITE

class Game:
    """
    A Bound Game instance. This model holds the logic to play the game.
    """
    def __init__(self):
        self.board = Board()
        self.player = BLACK
        self.pieces = {}
        self.over = False

    def next_player(self):
        """Switch players."""
        self.player = WHITE if self.player == BLACK else BLACK

    def move(self, source: tuple, dest: tuple):
        """Makes a move and updates the state of the game."""
        self.board.move(self.player, source, dest)

        if (self.board.did_bound(dest)):
            self.over = True
            return

        self.next_player()

