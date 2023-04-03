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
    games = 4
    average_rounds = 0
    
    for i in range(games):
        print("Game: ", i)
        # create a game controller with two bots
        player1 = Bot(1,"Tiago")
        player1.bot_settings.minimax_depth = 5
        player1.bot_settings.minimax_evaluate = 3
        player1.bot_settings.montecarlo_exploration = 1.4
        player1.bot_settings.montecarlo_simulations = 500
        player2 = Bot(2,"Tiago")
        player2.bot_settings.minimax_depth = 5
        player2.bot_settings.minimax_evaluate = 3
        player2.bot_settings.montecarlo_exploration = 1.4
        player2.bot_settings.montecarlo_simulations = 500
        #board = 1 -> 4x5 board | board = 2 -> 6x5 board | board = 3 -> 8x5 board
        game_controller = GameController(player1, player2,None,1) 
        # play the game
        winner = game_controller.play()
        time_player_1 = game_controller.average_time_player_1
        time_player_2 = game_controller.average_time_player_2
        rounds = game_controller.rounds
        count += 1
        average_time_player_1 = ((count - 1) * average_time_player_1 + time_player_1) / count  # calculate running average
        average_time_player_2 = ((count - 1) * average_time_player_2 + time_player_2) / count  # calculate running average
        average_rounds = ((count - 1) * average_rounds + rounds) / count

        #keep track of the results
        if winner == 1:
            player1_wins += 1
        elif winner == 2:
            player2_wins += 1 
        
    #print the results
    print("\n\n\nFINAL RESULTS")
    print("Number of games: ", games)
    print("Average rounds: ", average_rounds)
    print("Player 1 BLACK wins: ", player1_wins)
    print("Player 2 WHITE wins: ", player2_wins)
    print("Average time player 1 BLACK: ", average_time_player_1)
    print("Average time player 2 WHITE: ", average_time_player_2)
    
    
    
    
    
    
    

main_dev()