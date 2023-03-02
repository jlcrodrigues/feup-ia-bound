from model.game import Game

class GameController:
    def __init__(self):
        self.game = Game()

    def move(self, source, dest):
        self.game.move(source, dest)

    def get_current_player(self):
        return self.game.player