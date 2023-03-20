from view.pages.menu import Menu
from view.gui import GUI
from view.theme import *
import pygame_menu

class GameView(Menu):
    """Renders the game page."""
    def __init__(self, gui, game):
        super().__init__(gui, False)
        self.game = game
        self.selected = None
        self.exit = False

        self.last_player = 1
        self.played_over_sound = False
        self.playing_color = PLAYER_1_COLOR

        if self.gui == None: return
        self.init_menu()

    def init_menu(self):
        self.menu.add.label(
            'bound',
            font_name=FONT_PATH,
            float=True,
            font_color=EMPTY_COLOR,
        )
        self.menu.add.button('').translate(-100, -100) # dummy button to avoid default selection
        self.menu.add.button(
            '<',
            lambda : self.close(),
            align=pygame_menu.locals.ALIGN_LEFT,
            float=True,
            font_color = EMPTY_COLOR,
            selection_color = SELECTED_COLOR
        )


    def step(self):
        if self.gui == None:
            return self.game.over

        self.step_sound()

        self.playing_color = PLAYER_1_COLOR if self.game.player == 1 else PLAYER_2_COLOR
        self.menu.get_widgets()[0].update({'font_color': self.playing_color})

        self.gui.draw_background()
        self.gui.draw_grid(self.game.board, self.selected)
        self.gui.draw_pieces(self.game.board)
        self.draw_bottom_text()
        self.gui.draw_menu(self.menu)        

        self.gui.update()

        self.gui.handle_events()

        return self.exit

    def step_sound(self):
        """Play sounds according to game state."""
        if (self.game.player != self.last_player):
            self.gui.sound.play_effect('move')
        self.last_player = self.game.player
        if (self.game.over and not self.played_over_sound):
            self.gui.sound.play_effect('bound')
            self.played_over_sound = True

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

    def close(self):
        """Exit to the menu."""
        self.gui.sound.toggle_menu()
        self.exit = True

    def draw_bottom_text(self):
        """Draws the text at the bottom of the screen depending on game state."""
        words = 'black to move' if self.game.player == 1 else 'white to move'
        if (self.game.over):
            words = 'black wins' if self.game.player == 1 else 'white wins'

        text = self.gui.font_small.render(words, True, self.playing_color)
        self.gui.win.blit(text, (self.gui.get_width() / 2 - text.get_width() / 2,
                                         self.gui.get_height() - text.get_height()))

