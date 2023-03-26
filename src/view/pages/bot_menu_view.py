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
        
        self.minimax_depth = 3
        self.minimax_evaluate = 3
        self.montecarlo_exploration = 2.5
        self.montecarlo_simulations = 2500

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
        
        self.menu.add.range_slider('Minimax Depth:',
                                      range_values=[1,2,3,4,5],
                                      range_text_value_enabled=False,
                                      range_text_value_tick_hfactor=0.1,
                                      default=self.minimax_depth,
                                      onchange=self.change_minimax_depth)
        
        self.menu.add.selector('Evaluation Function: ',
                            [('Basic', 1),
                            ('Intermediate', 2),
                            ('Advanced', 3)],
                            default=self.minimax_evaluate-1,
                            onchange=self.change_minimax_evalutate)
        
        self.menu.add.range_slider('Montecarlo exploration:',
                                      range_values=[1.4,2.5,4],
                                      range_text_value_enabled=False,
                                      range_text_value_tick_hfactor=0.1,
                                      default=self.montecarlo_exploration,
                                      onchange=self.change_montecarlo_exploration)
                
        self.menu.add.range_slider('Montecarlo simulations:',
                                      range_values=[500,1500,2500,5000],
                                      range_text_value_enabled=False,
                                      range_text_value_tick_hfactor=0.1,
                                      default=self.montecarlo_simulations,
                                      onchange=self.change_montercarlo_simulations)
        
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
        
    def change_minimax_depth(self,new_depth: int):
        self.minimax_depth = new_depth
        self.play_click()
        
    def change_minimax_evalutate(self, _, new_evaluate: int):
        self.minimax_evaluate = new_evaluate
        self.play_click()
        
    def change_montecarlo_exploration(self,new_exploration: float):
        self.montecarlo_exploration = new_exploration
        self.play_click()
        
    def change_montercarlo_simulations(self,new_simulations: int):
        self.montecarlo_simulations = new_simulations
        self.play_click()

    def start_game(self):
        self.menu.disable()
        self.gui.sound.toggle_game()
        self.start = True

    def close(self):
        self.menu.disable()
        self.start = False
