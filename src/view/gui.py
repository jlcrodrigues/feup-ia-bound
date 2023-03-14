import pygame
from math import sin, cos

from model.game import Game
from model.board import Board
from view.theme import *

class GUI:
    """
    This class defines all the functions related to ui.
    This works as an abstraction to pygame and it should only be used here as well.
    """
    def __init__(self):
        pygame.init()

        self.win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Bound")
        # TODO icon = pygame.image.load("../assets/images/icon.png")
        # pygame.display.set_icon(icon)
        self.clock = pygame.time.Clock()

        self.background = pygame.image.load("../assets/images/background.png")

        self.mouse_pos = (-1, -1)
        self.mouse_pressed = (False, False, False)

        #self.font = pygame.font.Font('../assets/fonts/immortal/IMMORTAL.ttf', 30)
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
        #self.clock.tick(60)

    def draw_menu(self, menu):
        if menu.is_enabled():
            menu.update(self.events)
            menu.draw(self.win)

    def draw_grid(self, board, selected: tuple):
        """Display the board, including nodes, pieces and edges."""
        gap = (self.win.get_width() - PADDING) / (board.ring_number * 2)
        center = (self.win.get_width() / 2, self.win.get_height() / 2)
        pygame.draw.circle(self.win, EMPTY_COLOR, center, gap * board.ring_number + PIECE_RADIUS / 2 , LINE_WIDTH)
        for node in board.nodes:
            pos = self.get_pos(board, (node.level, node.pos))
            for edge in node.edges:
                edge_coords = board.to_coords(edge)
                if edge_coords[0] == board.ring_number - 1:
                    continue
                edge_pos = self.get_pos(board, edge_coords)
                
                line_color = EMPTY_COLOR
                if board.nodes[edge].is_empty() and (node.level, node.pos) == selected:
                    line_color = SELECTED_COLOR 
                if board.to_coords(edge) == selected and node.is_empty():
                    line_color = SELECTED_COLOR 

                pygame.draw.line(self.win, line_color, pos, edge_pos, LINE_WIDTH)

    def draw_pieces(self, board):
        """Display the board, including nodes, pieces and edges."""
        for node in board.nodes:
            pos = self.get_pos(board, (node.level, node.pos))

            pygame.draw.circle(self.win, EMPTY_COLOR, pos , NODE_RADIUS)
            if not node.is_empty():
                pygame.draw.circle(self.win, self.get_color(node), pos , PIECE_RADIUS)


    def get_pos(self, board: Board, coords: tuple):
        """
        Get the screen coordinates from a tuple of board coordinates.
        Returns a tuple of the form (x, y)
        """
        center = (self.win.get_width() / 2, self.win.get_height() / 2)
        gap = (self.win.get_width() - PADDING) / (board.ring_number * 2) # gap between levels
        angle = 2 * 3.14 / board.nodes_per_ring
        offset = angle / 2 * (coords[0] // 2)
        x = cos(offset + coords[1] * angle) * (coords[0] + 1) * gap + center[0]
        y = sin(offset + coords[1] * angle) * (coords[0] + 1) * gap + center[1]
        return (int(x), int(y))

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



