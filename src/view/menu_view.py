import pygame
import pygame_menu

class MenuView:
    def __init__(self, gui):
        self.gui = gui
        self.mode = 1
        self.start = False

        self.menu = pygame_menu.Menu('Bound', 400, 300,
                       theme=pygame_menu.themes.THEME_ORANGE)

        self.init_menu()

    def init_menu(self):
        self.menu.add.selector('',
            [('Player vs Player', 1),
              ('Player vs Cpu', 2),
              ('CPU vs Cpu', 3)],
                onchange = self.change_mode)
        self.menu.add.button('Play', self.start_game)
        self.menu.add.button('Quit', pygame_menu.events.EXIT)


    def step(self) -> bool:
        self.menu.mainloop(self.gui.win)
        return self.start

    def change_mode(self, _, new_mode: int):
        self.mode = new_mode

    def start_game(self):
        self.menu.disable()
        self.start = True
