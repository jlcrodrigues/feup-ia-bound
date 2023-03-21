import pygame_menu
from view.pages.menu import Menu
from view.theme import *

class MenuView(Menu):
    """Renders the main menu."""
    def __init__(self, gui):
        super().__init__(gui)
        self.mode = 1
        self.start = False

        self.init_menu()
        self.menu.center_content()

    def init_menu(self):
        """Define all the widgets needed on the menu."""
        self.menu.add.label(
            'bound',
            font_name=FONT_PATH,
            font_size=80)

        self.menu.add.selector('',
            [('Player vs Player', 1),
              ('Player vs Cpu', 2),
              ('CPU vs Cpu', 3)],
                onchange = self.change_mode)
        self.menu.add.button('play', self.start_game)
        self.menu.add.button('quit', pygame_menu.events.EXIT)

    def step(self) -> bool:
        """Calls the menu main loop."""
        self.menu.mainloop(self.gui.win)
        return self.start

    def change_mode(self, _, new_mode: int):
        self.play_click()
        self.mode = new_mode

    def start_game(self):
        self.menu.disable()
        if self.mode == 1:
            self.gui.sound.toggle_game()
        self.start = True