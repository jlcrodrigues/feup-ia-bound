import pygame_menu
from view.theme import *

class MenuView:
    def __init__(self, gui):
        self.gui = gui
        self.mode = 1
        self.start = False

        self.init_theme()
        self.menu = pygame_menu.Menu('', gui.get_width(), gui.get_height(),
                       theme=self.theme)

        self.init_menu()

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

    def init_theme(self):
        """Define the menu theme."""
        self.theme = pygame_menu.Theme()
        self.theme.widget_font_color = EMPTY_COLOR
        self.theme.selection_color = SELECTED_COLOR

        self.theme.background_color = pygame_menu.BaseImage(
            image_path="../assets/images/background.png"
        )
        self.theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE
        self.theme.title_font = self.gui.font
        self.theme.widget_font = self.gui.font

    def step(self) -> bool:
        """Calls the menu main loop."""
        self.menu.mainloop(self.gui.win)
        return self.start

    def change_mode(self, _, new_mode: int):
        self.mode = new_mode

    def start_game(self):
        self.menu.disable()
        if self.mode == 1:
            self.gui.sound.toggle_game()
        self.start = True
