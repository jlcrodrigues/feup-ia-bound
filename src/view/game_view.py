from view.gui import GUI
from view.theme import *
import pygame_menu

class GameView():
    def __init__(self, gui, game):
        self.gui = gui
        self.game = game
        self.selected = None
        self.exit = False

        theme = pygame_menu.Theme()
        theme.title = False  # Hide the menu title
        theme.background_color = (0,0,0,0)
        theme.border_width = 0
        theme.widget_box_arrow_color = (0,0,0,0)

        self.playing_color = PLAYER_1_COLOR

        self.menu = pygame_menu.Menu('', gui.get_width(), gui.get_height(),
                                     theme=theme, center_content=False)
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
        if self.gui == None: return True

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

