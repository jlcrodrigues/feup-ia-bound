class BotSettings:
    """BotSettings class
        minimax_depth: depth of the minimax algorithm
        minimax_evaluate: function used to evaluate the board(1 for easy, 2 for medium, 3 for hard)
        montecarlo_exploration: exploration constant used in the montecarlo algorithm
        montecarlo_simulations: number of simulations used in the montecarlo algorithm
    """
    def __init__(self,minimax_depth=3,minimax_evaluate=3,montecarlo_exploration=2.5,montecarlo_simulations=2500):
        self.minimax_depth = minimax_depth
        self.minimax_evaluate = minimax_evaluate
        self.montecarlo_exploration = montecarlo_exploration
        self.montecarlo_simulations = montecarlo_simulations