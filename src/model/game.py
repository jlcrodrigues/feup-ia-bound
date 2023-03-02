from board import Board, BLACK, WHITE

class Game:
    def __init__(self):
        self.board = Board()
        self.player = BLACK
        self.pieces = {}

    def next_player(self):
        """Switch players."""
        self.player = WHITE if self.player == BLACK else BLACK

    def move(self, source: int, dest: int):
        self.board.move(self.player, source, dest)

