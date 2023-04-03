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
    average_time_player_1 = 0
    average_time_player_2 = 0
    count = 0
    games = 2
    
    for i in range(games):
        print("Game: ", i)
        # create a game controller with two bots
        player1 = Bot(1,"Tiago")
        player1.bot_settings.montecarlo_exploration = 2
        player1.bot_settings.montecarlo_simulations = 2000
        player2 = Bot(2,"Martim")
        player2.bot_settings.minimax_depth = 3
        player2.bot_settings.minimax_evaluate = 3
        #board = 1 -> 4x5 board | board = 2 -> 6x5 board | board = 3 -> 8x5 board
        game_controller = GameController(player1, player2,None,1) 
        # play the game
        winner = game_controller.play()
        time_player_1 = game_controller.average_time_player_1
        time_player_2 = game_controller.average_time_player_2
        count += 1
        average_time_player_1 = ((count - 1) * average_time_player_1 + time_player_1) / count  # calculate running average
        average_time_player_2 = ((count - 1) * average_time_player_2 + time_player_2) / count  # calculate running average

        #keep track of the results
        if winner == 1:
            player1_wins += 1
        elif winner == 2:
            player2_wins += 1 
        
    #print the results
    print("\n\n\nFINAL RESULTS")
    print("Number of games: ", games)
    print("Player 1 wins: ", player1_wins)
    print("Player 2 wins: ", player2_wins)
    print("Average time player 1: ", average_time_player_1)
    print("Average time player 2: ", average_time_player_2)
    
    
    
    
    
    
    

main_dev()