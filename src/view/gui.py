import pygame
from math import sin, cos
import os

from model.game import Game
from model.board import Board
from model.settings import Settings
from view.theme import *
from view.gui_sound import GUISound

class GUI:
    """
    This class defines all the functions related to ui.
    This works as an abstraction to pygame and it should only be used here as well.
    """
    def __init__(self):
        pygame.init()

        self.win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Bound")
        icon = pygame.image.load("../assets/images/icon.png")
        pygame.display.set_icon(icon)
        self.clock = pygame.time.Clock()

        self.closed = False

        self.settings = Settings()
        self.sound = GUISound(self.settings)
        
        self.background = pygame.image.load("../assets/images/background.png")

        self.skin = "Default"
        self.set_skin("default")

        self.mouse_pos = (-1, -1)
        self.mouse_pressed = (False, False, False)

        self.font = pygame.font.Font(FONT_PATH, 30)
        self.font_small = pygame.font.Font(FONT_PATH, 20)
        self.events = []


    def handle_events(self):
        """Fetch events from the GUI."""
        self.mouse_pressed = (False, False, False)
        self.events = pygame.event.get()
        for event in self.events:
            if event.type == pygame.QUIT:
                self.close()
                self.closed = True
                return False
            if event.type == pygame.VIDEORESIZE:
                old_win = self.win
                self.win = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                self.win.blit(old_win, (0,0))
                del old_win

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_pos = pygame.mouse.get_pos()
                self.mouse_pressed = pygame.mouse.get_pressed()
                
        return True

    def draw_background(self):
        """Display the background."""
        self.win.blit(self.background, (0, 0))

    def update(self):
        """Update the GUI."""
        pygame.display.update()
        self.clock.tick(60)

    def draw_menu(self, menu):
        if menu.is_enabled():
            menu.draw(self.win)
            menu.update(self.events)

    def draw_grid(self, board, selected: tuple):
        """Display the board, including nodes, pieces and edges."""
        gap = (self.win.get_width() - PADDING) / (board.ring_number * 2)
        center = self.get_board_center()
        angle = 2 * 3.14 / board.nodes_per_ring
        for node in board.nodes:
            pos = self.get_pos(board, (node.level, node.pos))
            for edge in node.edges:
                edge_coords = board.to_coords(edge)
                edge_pos = self.get_pos(board, edge_coords)
                
                line_color = EMPTY_COLOR
                if board.nodes[edge].is_empty() and (node.level, node.pos) == selected:
                    line_color = SELECTED_COLOR 
                if board.to_coords(edge) == selected and node.is_empty():
                    line_color = SELECTED_COLOR 

                #draw the arches
                if edge_coords[0] == board.ring_number - 1 and node.level == board.ring_number - 1:
                    #only draw clockwise
                    if node.pos == board.nodes_per_ring - 1 and edge_coords[1] == 0: start_pos = -1
                    elif node.pos == 0 and edge_coords[1] == board.nodes_per_ring - 1: continue
                    elif node.pos > edge_coords[1]: continue 

                    #get the start angle
                    else: start_pos = node.pos if node.pos < edge_coords[1] else edge_coords[1]
                    start_angle = angle * (-start_pos - 1) + (angle / 2) * (node.level // 2)

                    rectangle = (center[0] - gap * board.ring_number - 4, center[1] - gap * board.ring_number - 4,
                                  gap * board.ring_number * 2 + 4, gap * board.ring_number * 2 + 4)
                    pygame.draw.arc(self.win, line_color, rectangle , start_angle - angle, start_angle, LINE_WIDTH)
                        
                else: pygame.draw.line(self.win, line_color, pos, edge_pos, LINE_WIDTH)

    def draw_pieces(self, board, last_moved: tuple):
        """Display the board, including nodes, pieces and edges."""
        for node in board.nodes:
            pos = self.get_pos(board, (node.level, node.pos))

            pygame.draw.circle(self.win, EMPTY_COLOR, pos , NODE_RADIUS)
            if not node.is_empty():
                if node.piece == 1:
                #pygame.draw.circle(self.win, self.get_color(node), pos , PIECE_RADIUS)
                    self.win.blit(self.black_img, (pos[0] - 16, pos[1] - 16))
                else: 
                    self.win.blit(self.white_img, (pos[0] - 16, pos[1] - 16))

            elif last_moved == (node.level, node.pos):
                pygame.draw.circle(self.win, EMPTY_COLOR2, pos , NODE_RADIUS)


    def get_pos(self, board: Board, coords: tuple):
        """
        Get the screen coordinates from a tuple of board coordinates.
        Returns a tuple of the form (x, y)
        """
        center = self.get_board_center()
        gap = (self.win.get_width() - PADDING) / (board.ring_number * 2) # gap between levels
        angle = 2 * 3.14 / board.nodes_per_ring
        offset = angle / 2 * (coords[0] // 2)
        x = cos(offset + coords[1] * angle) * (coords[0] + 1) * gap + center[0]
        y = sin(offset + coords[1] * angle) * (coords[0] + 1) * gap + center[1]
        return (int(x), int(y))

    def get_board_center(self) -> (int):
        return (self.win.get_width() / 2, self.win.get_height() / 2 -0* 0.3 * PADDING)

    def get_color(self, node):
        """Get the current color of a node."""
        if node.piece == 1:
            return PLAYER_1_COLOR
        elif node.piece == 2:
            return PLAYER_2_COLOR
        else:
            return EMPTY_COLOR

    def close(self):
        """Handles user exiting the game."""
        pygame.quit()

    def get_width(self):
        return self.win.get_width()

    def get_height(self):
        return self.win.get_height()

    def set_skin(self, skin):
        if not os.path.isfile("../assets/images/skins/" + skin + "/black.png"):
            print("That skin does not exist: " + skin)
            return

        self.skin = skin
        self.black_img = pygame.image.load("../assets/images/skins/" + skin + "/black.png")
        self.white_img = pygame.image.load("../assets/images/skins/" + skin + "/white.png")

        piece_size = 32
        self.black_img = pygame.transform.scale(self.black_img, (piece_size, piece_size))
        self.white_img = pygame.transform.scale(self.white_img, (piece_size, piece_size))
