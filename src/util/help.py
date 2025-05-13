from util.cell import Cell

class Help:
    def __init__(self):
        pass

    replace_cell = {
        Cell.X: "1",
        Cell.O: "2",
        Cell.NONE: "0"
    }

    def print_eval_board(self, board):
        print()
        for row in board:
            for cell in row:
                print(f"{cell:>3} ", end="")
            print()
        print()

    def print_board(self, board):
        print()
        for row in board:
            for cell in row:
                print(f"{self.replace_cell[cell]:>3} ", end="")
            print()
        print()
