from model.game import Game
from model.bot import Bot
from model.player import Player
from view.pages.game_view import GameView
from time import sleep,time

class GameController:
    """
    Controls the game flow. Connects view to the model.
    Can be executed without a view, so the bots are easier to test.
    Players can either be a Bot instance or None (for human players).
    """
    def __init__(self, player_1: Player, player_2: Player, gui=None, board=1):
        if (gui == None and (player_1 == None or player_2 == None)):
            raise ValueError("If no GUI is provided, both players must be bots.")
        board_size = board if gui == None else gui.settings.board_size
        self.game = Game(board_size)
        self.players = {}
        self.rounds = 0
        self.close = False
        self.gui = gui

        self.player_1 = player_1
        self.player_2 = player_2
        self.player = self.player_1
        self.last_moved = None

        self.view = GameView(gui, self.game, [player_1, player_2])
        
        self.average_time_player_1 = 0
        self.player_1_count = 0
        self.average_time_player_2 = 0
        self.player_2_count = 0

    def play(self):
        """Play out a full game."""
        while (not self.close):
            self.step()
        
        return self.game.winner

    def step(self):
        """Play one round of the game."""
        self.close = self.view.step(self.last_moved)

        if (self.view.is_restart):
            self.game = Game(self.gui.settings.board_size)
            self.view.restart(self.game)
            self.rounds = 0
            self.last_moved = None
            self.player = self.player_1
            return

        if (self.game.over): return
        if self.view.can_move():
            if self.step_move():
                self.rounds += 1

    def step_move(self):
        """Execute a move given by the current player."""
        if self.player.is_bot: 
            delay = 0 if self.gui == None else self.gui.settings.bot_delay_in_sec()
            start_time = time()
            next_move = self.player.get_move(self.game)
            end_time = time()  # get time after function completes
            elapsed_time = end_time - start_time  # calculate elapsed time
            
            if self.player == self.player_1:
                self.player_1_count += 1  # increment count
                self.average_time_player_1 = ((self.player_1_count - 1) * self.average_time_player_1 + elapsed_time) / self.player_1_count  # calculate running average
            elif self.player == self.player_2:
                self.player_2_count += 1  # increment count
                self.average_time_player_2 = ((self.player_2_count - 1) * self.average_time_player_2 + elapsed_time) / self.player_2_count  # calculate running average

            if elapsed_time < delay:
                sleep(delay - elapsed_time)  # wait for remaining time
        else:
            next_move = self.get_user_input()

        if next_move == None: return False

        self.game.move(next_move[0], next_move[1])
        self.last_moved = next_move[0]

        if (self.game.over):
            print("Game ended, winner: ", str(self.game.winner), " , rounds: " , str(self.rounds))
            print("Average time player 1: ", self.average_time_player_1)
            print("Average time player 2: ", self.average_time_player_2)
            return True

        self.next_player()
        return True

    def next_player(self):
        """Switch players."""
        self.player = self.player_2 if self.player == self.player_1 else self.player_1 

    def get_current_player(self):
        return self.game.player

    def get_user_input(self):
        """Get user input from the view."""
        return self.view.get_user_input()