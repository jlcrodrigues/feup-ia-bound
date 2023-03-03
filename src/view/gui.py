import pygame
from math import sin, cos
from model.game import Game
from model.board import Board

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

BACKGROUND_COLOR = (245, 155, 50)
EMPTY_COLOR = (240, 170, 76)
PLAYER_1_COLOR = (20, 20, 20)
PLAYER_2_COLOR = (237, 210, 187)

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

    def draw_game(self, game: Game):
        """Display current state of the game."""
        self.win.fill(BACKGROUND_COLOR)
        self.draw_board(game.board)
        pygame.display.update()

    def handle_events(self):
        """Fetch events from the GUI."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close()
                return False
            if event.type == pygame.VIDEORESIZE:
                old_win = self.win
                self.win = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                self.win.blit(old_win, (0,0))
                del old_win
                
        return True

    def draw_board(self, board):
        """Display the board, including nodes, pieces and edges."""
        for node in board.nodes:
            pos = self.get_pos(board, (node.level, node.pos))
            for edge in node.edges:
                edge_pos = self.get_pos(board, board.to_coords(edge))
                pygame.draw.line(self.win, EMPTY_COLOR, pos, edge_pos, 2)
            pygame.draw.circle(self.win, self.get_color(node), pos , 10)

    def get_pos(self, board: Board, coords: tuple):
        """
        Get the screen coordinates from a tuple of board coordinates.
        Returns a tuple of the form (x, y)
        """
        center = (self.win.get_width() / 2, self.win.get_height() / 2)
        gap = self.win.get_width() / (board.ring_number * 2) # gap between levels
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


