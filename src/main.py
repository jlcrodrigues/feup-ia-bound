from model.board import Board
from states.menu_state import MenuState
from view.gui import GUI

def main():
    gui = GUI()
    state = MenuState(gui)

    while (state != None):
        state = state.step()

if __name__ == "__main__":
    main()