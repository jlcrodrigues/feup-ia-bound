from model.board import Board
from states.game_state import GameState

def main():
    state = GameState()

    while (state != None):
        state = state.step()

if __name__ == "__main__":
    main()