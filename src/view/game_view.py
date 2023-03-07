from view.gui import GUI
from view.theme import *

class GameView():
    def __init__(self, gui, game):
        self.gui = gui
        self.game = game
        self.selected = None

    def step(self):
        if self.gui == None: return True
        self.gui.draw_game(self.game, self.selected)
        return self.gui.handle_events()

    def get_user_input(self):
        """Read the mouse state and determine if the player has made a move.
        The also view keeps the state of the selected piece in order to render possible moves.
        """
        player = self.game.player
        pieces = self.game.board.pieces[player]

        if (not self.gui.mouse_pressed[0]): return None

        mouse_pos =  self.gui.mouse_pos

        # select a piece
        for piece in pieces:
            piece_pos = self.gui.get_pos(self.game.board, piece)
            if self.dist(piece_pos, mouse_pos) < PIECE_RADIUS ** 2:
                self.selected = piece
                return None

        # make a move
        if self.selected != None:
            for edge in self.game.board.get_piece_moves(self.selected):
                edge_pos = self.gui.get_pos(self.game.board, edge)
                if self.dist(edge_pos, mouse_pos) < PIECE_RADIUS ** 2:
                    move =  (self.selected, edge)
                    self.selected = None
                    return move
        
        self.selected = None
            
    
    def dist(self, coord1: tuple, coord2: tuple):
        """Get the square distance between two points."""
        return (coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1])**2

