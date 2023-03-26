
BLACK = 1
WHITE = 2

class Player:
    def __init__(self, player):
        self.player = player
        self.is_bot = False
        self.name = "Player " + str(player)

