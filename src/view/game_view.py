from view.gui import GUI

class GameView():
    def __init__(self, gui, game):
        self.gui = gui
        self.game = game

    def step(self):
        if self.gui == None: return True
        self.gui.draw_game(self.game)
        return self.gui.handle_events()

