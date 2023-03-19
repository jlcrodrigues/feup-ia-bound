import pygame
import pygame_menu
from view.theme import *

class Menu:
    """This class defines a generic menu.
    Different pages can extend it in order to use the same menu theme.
    """
    def __init__(self, gui, background=True):
        self.gui = gui
        self.init_theme(background)

        self.menu = pygame_menu.Menu('', gui.get_width(), gui.get_height(),
                       theme=self.theme, center_content=False)
        
        self.init_sounds()


    def init_theme(self, background):
        """Define the menu theme."""
        self.theme = pygame_menu.Theme()
        self.theme.widget_font_color = EMPTY_COLOR
        self.theme.selection_color = SELECTED_COLOR
        self.theme.title = False  # Hide the menu title
        self.theme.widget_selection_effect = pygame_menu.widgets.SimpleSelection()

        if background:
            self.theme.background_color = pygame_menu.BaseImage(
                image_path="../assets/images/background.png"
            )
        else: 
            self.theme.background_color = (255,255,255,0)
        self.theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE
        self.theme.title_font = self.gui.font
        self.theme.widget_font = self.gui.font

    def init_sounds(self):
        engine = pygame_menu.sound.Sound()
        engine.set_sound(pygame_menu.sound.SOUND_TYPE_WIDGET_SELECTION, 
                         '../assets/sound/effects/click.mp3')

        self.menu.set_sound(engine, recursive=True)  # Apply on menu and all sub-menus
    
    def play_click(self):
        self.sound = pygame.mixer.Sound("../assets/sound/effects/click.mp3")
        self.sound.play()