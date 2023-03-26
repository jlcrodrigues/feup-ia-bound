import pygame_menu
from view.theme import *
from view.pages.menu import Menu

class SettingsMenuView(Menu):
    """Renders the settings menu."""
    def __init__(self, gui, text):
        super().__init__(gui)
        self.start = False
        self.text = text

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

        # Add a selector for the board size
        self.menu.add.selector('Board Size: ',
                            [('Normal', 1),
                                ('Large', 2),
                                ('Extra', 3)],
                            default=self.gui.settings.board_size-1,
                            onchange=self.change_board_size)
        
        self.menu.add.range_slider('Music Volume: ',
                                      range_values=[0,20,40,60,80,100],
                                      range_text_value_enabled=False,
                                      slider_text_value_enabled=False,
                                      range_text_value_tick_hfactor=0.1,
                                      default=self.gui.settings.music_volume*100,
                                      onchange=self.change_music_volume)
        
        self.menu.add.range_slider('Sound Effects: ',
                                      range_values=[0,20,40,60,80,100],
                                      range_text_value_enabled=False,
                                      slider_text_value_enabled=False,
                                      range_text_value_tick_hfactor=0.1,
                                      default=self.gui.settings.sound_effects_volume*100,
                                      onchange=self.change_effects_volume)
        
        self.menu.add.selector('Bot Speed: ',
                            [('Fast', 1),
                                ('Normal', 2),
                                ('Slow', 3)],
                            default=self.gui.settings.bot_delay-1,
                            onchange=self.change_bot_delay)
        
        self.menu.select_widget(self.menu.get_widgets()[2])

    def step(self) -> bool:
        """Calls the menu main loop."""
        self.menu.mainloop(self.gui.win)
        return self.start
    
    def change_board_size(self, _, new_size: int):
        self.play_click()
        self.gui.settings.board_size = new_size

    def change_music_volume(self,new_volume: int):
        self.play_click()
        self.gui.settings.music_volume = new_volume/100
        self.gui.sound.music.set_volume(new_volume/100)
        
    def change_effects_volume(self,new_volume: int):
        self.play_click()
        self.gui.settings.sound_effects_volume = new_volume/100
        self.init_sounds()
        
    def change_bot_delay(self, _, new_delay: int):
        self.play_click()
        self.gui.settings.bot_delay = new_delay

    def close(self):
        self.menu.disable()
        self.start = False
