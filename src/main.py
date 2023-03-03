from model.board import Board
from states.game_state import GameState
from view.gui import GUI

def main():
    gui = GUI()
    state = GameState(gui)

    while (state != None):
        state = state.step()

if __name__ == "__main__":
    main()