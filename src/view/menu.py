import pygame_menu
from view.theme import *

class Menu:
    def __init__(self, gui, background=True):
        self.gui = gui
        self.init_theme(background)
        self.menu = pygame_menu.Menu('', gui.get_width(), gui.get_height(),
                       theme=self.theme, center_content=False)

    def init_theme(self, background):
        """Define the menu theme."""
        self.theme = pygame_menu.Theme()
        self.theme.widget_font_color = EMPTY_COLOR
        self.theme.selection_color = SELECTED_COLOR
        self.theme.title = False  # Hide the menu title

        if background:
            self.theme.background_color = pygame_menu.BaseImage(
                image_path="../assets/images/background.png"
            )
        else: 
            self.theme.background_color = (255,255,255,0)
        self.theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE
        self.theme.title_font = self.gui.font
        self.theme.widget_font = self.gui.font