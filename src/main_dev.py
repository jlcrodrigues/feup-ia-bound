"""
This file can be used to better test the AI without the GUI.
"""

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

from model.bot import Bot
from controller.game_controller import GameController

def main_dev():
    player1_wins = 0
    player2_wins = 0
    games = 20
    
    for i in range(games):
        print("Game: ", i)
        # create a game controller with two bots
        game_controller = GameController(Bot(1,1), Bot(2,1))
        # play the game
        winner = game_controller.play()
        #keep track of the results
        if winner == 1:
            player1_wins += 1
        elif winner == 2:
            player2_wins += 1 
        
    #print the results
    print("Number of games: ", games)
    print("Player 1 wins: ", player1_wins)
    print("Player 2 wins: ", player2_wins)
    
    
    
    
    
    

main_dev()