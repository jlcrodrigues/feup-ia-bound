import pygame_menu
from view.theme import *
from view.pages.menu import Menu

TEXT_PATH = '../assets/text/about.txt'

class AboutView(Menu):
    """Renders the about page."""
    def __init__(self, gui, text):
        super().__init__(gui)
        self.start = False
        self.text = text
        
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
        
        self.menu.add.label(
            self.descriptions[0],
            wordwrap=True,
            font_name=FONT_PATH,
            font_size=25).set_padding([0, 0, 10, 10])

    def step(self) -> bool:
        """Calls the menu main loop."""
        self.menu.mainloop(self.gui.win)
        return self.start
    
    def load_texts(self):
        """Load about from file."""
        with open(TEXT_PATH, 'r') as file:
            self.descriptions.append(file.read())
            
    
    def close(self):
        self.menu.disable()
        self.start = False
