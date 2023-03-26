import pygame_menu
from view.theme import *
from view.pages.menu import Menu
from model.bot import Bot, BOTS

TEXT_PATH = '../assets/text/bot/'

class BotMenuView(Menu):
    """Renders the difficulty selection menu."""
    def __init__(self, gui, text='Choose diffifulty'):
        super().__init__(gui)
        self.gui = gui
        self.start = False
        self.text = text

        self.selection = next(iter(BOTS)) #first

        self.descriptions = []
        self.load_texts()

        self.init_menu()

    def init_menu(self):
        """Define all the widgets needed on the menu."""
        self.menu.add.button(
            '<',
            lambda : self.close(),
            align=pygame_menu.locals.ALIGN_LEFT,
            float=True,
            font_color = EMPTY_COLOR,
            selection_color = SELECTED_COLOR
        )
        self.menu.add.label(
            self.text,
            font_name=FONT_PATH,
            font_size=40)

        self.menu.add.selector('',
              [(b, b) for b in BOTS],
                onchange = self.change_bot,)
        self.menu.add.label(
            self.descriptions[0],
            font_name=FONT_PATH,
            font_size=25)
        self.menu.add.button('play', self.start_game).translate(0, PADDING)
         
        self.menu.select_widget(self.menu.get_widgets()[2])

    def load_texts(self):
        """Load bot descriptions from files."""
        for i in range(0, len(BOTS)):
            with open(TEXT_PATH + str(i) + '.txt', 'r') as file:
                self.descriptions.append(file.read())

    def step(self) -> bool:
        """Calls the menu main loop."""
        self.menu.mainloop(self.gui.win)
        return self.start

    def change_bot(self, _, new_bot: str):
        self.menu.get_widgets()[3].set_title(self.descriptions[BOTS[new_bot]])
        self.selection = new_bot
        self.play_click()

    def start_game(self):
        self.menu.disable()
        self.gui.sound.toggle_game()
        self.start = True

    def close(self):
        self.menu.disable()
        self.start = False
