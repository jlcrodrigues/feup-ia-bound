from model.board import Board

def main():
    board = Board(2,3)
    for i in board.nodes:
        print(i, sep=" ")
        print(i.edges)


if __name__ == "__main__":
    main()