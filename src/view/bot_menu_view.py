import pygame_menu
from view.theme import *

TEXT_PATH = '../assets/text/bot/'
MAX_DIFFICULTY = 2

class BotMenuView:
    def __init__(self, gui):
        self.gui = gui
        self.start = False

        self.selection = (0, 0) # (bot, diffculty)

        self.descriptions = []
        self.load_texts()

        self.init_theme()
        self.menu = pygame_menu.Menu('', gui.get_width(), gui.get_height(),
                       theme=self.theme)

        self.init_menu()

    def init_menu(self):
        """Define all the widgets needed on the menu."""
        self.bot_labels = [pygame_menu.widgets.Label('Hello'), pygame_menu.widgets.Label('World')]

        self.menu.add.label(
            'Choose bot diffifulty',
            font_name=FONT_PATH,
            font_size=40)

        self.menu.add.selector('',
            [('Tiago', 0),
              ('Martim', 1),
              ('Luis', 2)],
                onchange = self.change_bot)
        self.menu.add.button(
            '<',
            lambda : self.close(),
            align=pygame_menu.locals.ALIGN_LEFT,
            float=True,
            font_color = EMPTY_COLOR,
            selection_color = SELECTED_COLOR
        )
        self.menu.add.label(
            self.descriptions[0],
            font_name=FONT_PATH,
            font_size=30)
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
    
    def load_texts(self):
        """Load bot descriptions from files."""
        for i in range(0, MAX_DIFFICULTY + 1):
            with open(TEXT_PATH + str(i) + '.txt', 'r') as file:
                self.descriptions.append(file.read())

    def step(self) -> bool:
        """Calls the menu main loop."""
        self.menu.mainloop(self.gui.win)
        return self.start

    def change_bot(self, _, new_bot: int):
        self.menu.get_widgets()[3].set_title(self.descriptions[new_bot])
        self.selection = (new_bot, 0)

    def start_game(self):
        self.menu.disable()
        self.start = True

    def close(self):
        self.menu.disable()
        self.start = False
