from model.bot import Bot
from view.pages.menu import Menu
from view.gui import GUI
from view.theme import *
import pygame_menu
import pygame

class GameView(Menu):
    """Renders the game page."""
    def __init__(self, gui, game, players: list):
        super().__init__(gui, False)
        self.game = game
        self.selected = None
        self.exit = False
        self.is_restart = False

        self.last_player = 1
        self.played_over_sound = False
        self.playing_color = PLAYER_1_COLOR
        self.player1_name = players[0].name
        self.player2_name = players[1].name

        self.hint = None
        self.num_hints = 5
        self.pieces_index = 0 # used to cycle through the pieces history

        if self.gui == None: return
        self.init_menu()
        self.init_modal()

    def init_menu(self):
        """Create menu widgets."""
        self.menu.add.button('').translate(-100, -100) # dummy button to avoid default selection
        self.menu.add.button(
            '<',
            lambda : self.close(),
            align=pygame_menu.locals.ALIGN_LEFT,
            float=True,
            font_color = EMPTY_COLOR,
            selection_color = SELECTED_COLOR
        ).translate(0,-3)
        self.menu.add.label('bound', align=pygame_menu.locals.ALIGN_CENTER, float=True).translate(0,-3)
        self.menu.add.button(
            str(self.num_hints) + '?',
            lambda : self.show_hint() ,
            align=pygame_menu.locals.ALIGN_RIGHT,
            float=True,
            font_color = EMPTY_COLOR,
            font_size=100,
            selection_color = SELECTED_COLOR
        ).translate(-40,0)
        self.menu.add.button(
            '...',
            lambda : self.enable_modal(),
            align=pygame_menu.locals.ALIGN_RIGHT,
            float=True,
            font_color = EMPTY_COLOR,
            font_size=100,
            selection_color = SELECTED_COLOR
        ).translate(0,-10)
        
        history_y = self.gui.get_height() - FONT_SIZE - 20
        self.menu.add.button('<<', lambda : self.history_start(), float=True).translate(-FONT_SIZE*2, history_y)
        self.menu.add.button('<', lambda : self.history_backward(), float=True).translate(-FONT_SIZE/2, history_y)
        self.menu.add.button('>', lambda : self.history_forward(), float=True).translate(FONT_SIZE/2, history_y)
        self.menu.add.button('>>', lambda : self.history_current(), float=True).translate(FONT_SIZE*2, history_y)

    def init_modal(self):
        """Creates the pause modal box."""
        theme = self.theme 
        theme.widget_font_color = EMPTY_COLOR
        theme.selection_color = SELECTED_COLOR
        #theme.widget_selection_effect = pygame_menu.widgets.HighlightSelection()
        theme.background_color = pygame_menu.BaseImage(
                image_path="../assets/images/modal.png")
        self.modal = pygame_menu.Menu('', self.gui.get_width(), self.gui.get_height(),
                       theme=theme, center_content=True, enabled=False)

        self.modal.add.label('Paused').set_padding(30)
        self.modal.add.button('resume', lambda : self.disable_modal())
        self.modal.add.button('restart', lambda : self.enable_restart())
        self.modal.add.button('menu', lambda : self.close())
        self.modal.add.button('quit', pygame_menu.events.EXIT)

    def step(self, last_moved: tuple):
        if self.gui == None:
            return self.game.over

        if (self.game.player != self.last_player):
            if self.pieces_index == len(self.game.history) - 2: # update history
                self.pieces_index += 1

        self.update_modal()

        self.step_sound()

        #draw game
        self.gui.draw_background()
        self.gui.draw_grid(self.game.board, self.selected, self.hint)

        pieces = list(self.game.history.keys())[self.pieces_index]
        if (pieces[0] == '-'): pieces = pieces[1:]
        self.gui.draw_pieces(eval(pieces), self.game.board, last_moved)

        #draw ui
        self.draw_top_bar()
        self.draw_player_info()
        self.gui.draw_menu(self.modal)
        self.gui.draw_menu(self.menu)        

        self.gui.update()
        if not self.gui.handle_events(): self.exit = True

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
        if self.modal.is_enabled(): return None 
        player = self.game.player
        pieces = self.game.board.pieces[player]

        if (not self.gui.mouse_pressed[0]): return None

        mouse_pos =  self.gui.mouse_pos

        tolerance = 10

        # select a piece
        for piece in pieces:
            piece_pos = self.gui.get_pos(self.game.board, piece)
            if self.dist(piece_pos, mouse_pos) < (PIECE_RADIUS + tolerance) ** 2:
                self.selected = piece
                return None

        # make a move
        if self.selected != None:
            for edge in self.game.board.get_piece_moves(self.selected):
                edge_pos = self.gui.get_pos(self.game.board, edge)
                if self.dist(edge_pos, mouse_pos) < (PIECE_RADIUS + tolerance) ** 2:
                    move =  (self.selected, edge)
                    self.selected = None
                    self.hint = None
                    return move
        
        self.selected = None

    def update_modal(self):
        title = "Paused"
        if self.game.over:
            if self.game.winner == 1:
                title = self.player1_name + ' wins!'
            elif self.game.winner == 2:
                title = self.player2_name + ' wins!'
            else:
                title =  'Draw!'
        
        self.modal.get_widgets()[0].set_title(title)
        if (self.game.over and not self.played_over_sound): #using sound boolean to open modal once
            self.gui.mouse_pressed = (False, False, False)
            self.enable_modal()

    def restart(self, game):
        """Restart the game."""
        self.game = game
        self.last_player = 1
        self.is_restart = False 
        self.played_over_sound = False
        self.num_hints = 5
        self.menu.get_widgets()[3].set_title(str(self.num_hints) + '?')
        self.pieces_index = 0 
    
    def dist(self, coord1: tuple, coord2: tuple):
        """Get the square distance between two points."""
        return (coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1])**2

    def close(self):
        """Exit to the menu."""
        self.gui.sound.toggle_menu()
        self.exit = True

    def enable_restart(self):
        """Called when restart button is clicked. Tells the contorller to restart the game."""
        self.disable_modal()
        self.is_restart = True

    def enable_modal(self):
        """Enable the modal box."""
        self.modal.enable()
        #self.menu.disable()

    def disable_modal(self):
        """Disable the modal box."""
        self.modal.disable()
        #self.menu.enable()
        self.menu.get_widgets()[0].select(update_menu=True)
    
    def show_hint(self):
        if self.num_hints > 0:
            bot = Bot(self.last_player, "Martim")
            self.hint = bot.get_move(self.game)
            self.num_hints -= 1
            self.menu.get_widgets()[3].set_title(str(self.num_hints) + '?')

    def draw_top_bar(self):
        """Draw the top nav bar."""
        height = 0.3 * PADDING
        y = self.gui.get_height() - 0.3 * PADDING

        player_width = 110
        if self.game.over: return
        pygame.draw.rect(self.gui.win, SELECTED_COLOR if self.game.player == 1 else BACKGROUND_COLOR,
                        [0, y, player_width, height], 
                        border_bottom_right_radius=5, border_top_right_radius=5)

        pygame.draw.rect(self.gui.win, SELECTED_COLOR if self.game.player == 2 else BACKGROUND_COLOR,
                        [self.gui.get_width() - player_width, y, player_width, height],
                            border_bottom_left_radius=5, border_top_left_radius=5)

    def draw_player_info(self):
        """Draws the current player info."""
        px = 0.1 * PADDING
        py = self.gui.get_height() - 0.25 * PADDING 

        text1 = self.gui.font_small.render(self.player1_name, True, PLAYER_1_COLOR)

        text2 = self.gui.font_small.render(self.player2_name, True, PLAYER_2_COLOR)

        self.gui.win.blit(text1, (px, py))
        self.gui.win.blit(text2, (-px + self.gui.get_width() - text2.get_width(),py))

    def history_start(self):
        """Start the history."""
        self.pieces_index = 0
    
    def history_forward(self):
        """Move the history forward."""
        if self.pieces_index < len(self.game.history) - 1:
            self.pieces_index += 1
    
    def history_backward(self):
        """Move the history backward."""
        if self.pieces_index > 0:
            self.pieces_index -= 1
    
    def history_current(self):
        """Move the history to the current state."""
        self.pieces_index = len(self.game.history) - 1

    def can_move(self):
        """Check if the player can move."""
        return self.pieces_index == len(self.game.history) - 1
        