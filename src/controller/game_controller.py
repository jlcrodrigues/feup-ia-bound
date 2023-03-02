from model.game import Game
from model.bot import Bot

class GameController:
    def __init__(self):
        self.game = Game()
        self.players = {}

    def play(self):
        # display & fetch movement
        #self.game.move
        player_1 = Bot(1, 0)
        player_2 = Bot(2, 0)
        counter = 0
        while (not self.game.over):
            counter += 1
            next_move = player_1.get_move(self.game.board)
            self.game.move(next_move[0], next_move[1])
            if (self.game.over): break
            print(next_move)

            next_move = player_2.get_move(self.game.board)
            self.game.move(next_move[0], next_move[1])
            print(next_move)

        print("Game ended, winner: ", str(self.game.player), " , rounds: " , str(counter))

        return 1


    def get_current_player(self):
        return self.game.player