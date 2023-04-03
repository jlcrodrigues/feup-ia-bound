import pygame_menu
from view.pages.menu import Menu
from view.theme import *

class MenuView(Menu):
    """Renders the main menu."""
    def __init__(self, gui):
        super().__init__(gui)
        self.mode = 1
        self.start = False
        self.settings = False
        self.rules = False
        self.about = False

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
        
        self.menu.add.button('rules', self.start_rules)
        
        self.menu.add.button('settings', self.start_settings)
        
        self.menu.add.button('quit', pygame_menu.events.EXIT)
        
        self.menu.add.button(
            '@',
            lambda : self.start_about(),
            align=pygame_menu.locals.ALIGN_RIGHT,
            float=True,
            font_color = EMPTY_COLOR,
            font_size=100,
            selection_color = SELECTED_COLOR
        ).translate(-0,-420)

    def step(self) -> bool:
        """Calls the menu main loop."""
        self.menu.mainloop(self.gui.win)
        return self.start or self.settings

    def change_mode(self, _, new_mode: int):
        self.play_click()
        self.mode = new_mode

    def start_game(self):
        self.menu.disable()
        if self.mode == 1:
            self.gui.sound.toggle_game()
        self.start = True
        
    def start_settings(self):
        self.menu.disable()
        self.settings = True
        
    def start_rules(self):
        self.menu.disable()
        self.rules = True
        
    def start_about(self):
        self.menu.disable()
        self.about = True
