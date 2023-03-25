import pygame_menu
from view.pages.menu import Menu
from view.theme import *

class MenuView(Menu):
    """Renders the main menu."""
    def __init__(self, gui):
        super().__init__(gui)
        self.mode = 1
        self.start = False
        self.board_size = 1
        self.volume = 40
        self.effects = 40

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
        
        # Add a selector for the board size
        self.menu.add.selector('Board Size: ',
                            [('Normal', 1),
                                ('Large', 2),
                                ('Extra', 3)],
                            onchange=self.change_board_size)
        
        self.menu.add.range_slider('Music Volume: ',
                                      range_values=[0,20,40,60,80,100],
                                      range_text_value_enabled=False,
                                      slider_text_value_enabled=False,
                                      range_text_value_tick_hfactor=0.1,
                                      default=40,
                                      onchange=self.change_music_volume)
        
        self.menu.add.range_slider('Sound Effects: ',
                                      range_values=[0,20,40,60,80,100],
                                      range_text_value_enabled=False,
                                      slider_text_value_enabled=False,
                                      range_text_value_tick_hfactor=0.1,
                                      default=40,
                                      onchange=self.change_effects_volume)
        
        self.menu.add.button('quit', pygame_menu.events.EXIT)

    def step(self) -> bool:
        """Calls the menu main loop."""
        self.menu.mainloop(self.gui.win)
        return self.start

    def change_mode(self, _, new_mode: int):
        self.play_click()
        self.mode = new_mode
        
    def change_board_size(self, _, new_size: int):
        self.play_click()
        self.board_size = new_size

    def change_music_volume(self,new_volume: int):
        self.play_click()
        self.volume = new_volume
        self.gui.sound.music_volume = self.volume/100
        self.gui.sound.music.set_volume(self.volume/100)
        
    def change_effects_volume(self,new_effects_volume: int):
        self.play_click()
        self.effects = new_effects_volume
        self.gui.sound.effects_volume = self.effects/100
        self.init_sounds()

    def start_game(self):
        self.menu.disable()
        if self.mode == 1:
            self.gui.sound.toggle_game()
        self.start = True
