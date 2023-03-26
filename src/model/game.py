from model.board import Board, BLACK, WHITE, DRAW


class Game:
    """
    A Bound Game instance. This model holds the logic to play the game.
    """
    def __init__(self,board_size):
        self.board = self.init_board(board_size)
        self.player = BLACK
        self.winner = None
        self.over = False
        self.history = {}
        self.history[str(self.board.pieces)] = 1
        
    def init_board(self,board_size):
        if (board_size==1):
            return Board(4,5)
        elif(board_size==2):  
            return Board(6,5)
        elif(board_size==3):
            return Board(8,5)

    def next_player(self):
        """Switch players."""
        self.player = WHITE if self.player == BLACK else BLACK

    def move(self, source: tuple, dest: tuple):
        """Makes a move and updates the state of the game."""
        if source == None or dest == None:
            raise Exception("Trying to move null play.")
        self.board.move(self.player, source, dest)
        
        game_over, piece = self.board.did_bound(dest)
        
        
        if(self.stalemate()):
            self.over = True
            self.winner = DRAW
            return
        
        if (game_over):
            self.over = True
            #print(f"Piece {piece} bound!")
            bounded = self.board.nodes[self.board.to_index(piece)].piece
            self.winner = WHITE if bounded == BLACK else BLACK 
            return

        self.next_player()

    def stalemate(self):
        """Check if the game is in a stalemate."""
        
        #sort pieces
        sorted_pieces = {BLACK: sorted(self.board.pieces[BLACK]), WHITE: sorted(self.board.pieces[WHITE])}
        
        # Update the count for the current board
        if str(sorted_pieces) in self.history:
            self.history[str(sorted_pieces)] += 1
        else:
            self.history[str(sorted_pieces)] = 1

        if self.history[str(sorted_pieces)] == 3:
            return True
        
        return False