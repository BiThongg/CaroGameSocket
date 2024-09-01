
from re import X
import time

O = "O"
X = "X"


class CaroGame:
    X = "X"
    O = "O"
    EMPTY = None
    sizeMatrix = 6
    board = []

    def __init__(self):
        self.initialize_game()

    def initialize_game(self):
        self.board = [
            [CaroGame.EMPTY for _ in range(CaroGame.sizeMatrix)]
            for _ in range(CaroGame.sizeMatrix)
        ]

    def draw_board(self):
        for i in range(0, self.sizeMatrix):
            for j in range(0, self.sizeMatrix):
                print("{}|".format(self.board[i][j]), end=" ")
            print()
        print()

    def actions(self, board):
        possible_actions = set()

        for i in range(self.sizeMatrix):
            for j in range(self.sizeMatrix):
                if board[j][i] == self.EMPTY:
                    possible_actions.add((j, i))

        return possible_actions

    def result(self, board, action):
        if action not in self.actions(board):
            raise Exception("Invalid action")

        new_board = [row[:] for row in board]

        new_board[action[0]][action[1]] = self.player(self.board)

        return new_board

    def player(self, board):
        """
        Returns player who has the next turn on a board.
        """

        x_count = 0
        o_count = 0

        for i in range(self.sizeMatrix):
            for j in range(self.sizeMatrix):
                if board[j][i] == self.X:
                    x_count += 1
                elif board[j][i] == self.O:
                    o_count += 1

        print(x_count, o_count)

        if x_count > o_count:
            return self.O
        else:
            return self.X

    def terminal(self, board):
        if self.winner(board) is not None:
            return True

        for i in range(self.sizeMatrix):
            for j in range(self.sizeMatrix):
                if board[j][i] == self.EMPTY:
                    return False

        return True

    def winner(self, board):
        # caro _sizex15, 5 for win
        _size = self.sizeMatrix
        EMPTY = None
        board = self.board

        for i in range(_size):
            for j in range(_size):
                if board[i][j] != EMPTY:
                    # check horizontal
                    if j < _size - 4:
                        if (
                            board[i][j]
                            == board[i][j + 1]
                            == board[i][j + 2]
                            == board[i][j + 3]
                            == board[i][j + 4]
                        ):
                            return board[i][j]
                    # check vertical
                    if i < _size - 4:
                        if (
                            board[i][j]
                            == board[i + 1][j]
                            == board[i + 2][j]
                            == board[i + 3][j]
                            == board[i + 4][j]
                        ):
                            return board[i][j]
                    # check diagonal
                    if i < _size - 4 and j < _size - 4:
                        if (
                            board[i][j]
                            == board[i + 1][j + 1]
                            == board[i + 2][j + 2]
                            == board[i + 3][j + 3]
                            == board[i + 4][j + 4]
                        ):
                            return board[i][j]
                    if i < _size - 4 and j > 4:
                        if (
                            board[i][j]
                            == board[i + 1][j - 1]
                            == board[i + 2][j - 2]
                            == board[i + 3][j - 3]
                            == board[i + 4][j - 4]
                        ):
                            return board[i][j]

                    return None
    def utility(self, board):
                if self.winner(board) == self.X:
                    return 1
                elif self.winner(board) == self.O:
                    return -1
                else:
                    return 0

    def minimax(self, board):
        return 1

    def max_alpha_beta(self, alpha, beta):
        max_v = -2
        px = None
        py = None
        
        result = self.winner(self.board)
        if result == self.X:
            return (1, 0, 0)
        elif result == self.O:
            return (-1, 0, 0)
        elif result == None:
            return 0
        
        for i in range(0, self.sizeMatrix):
            for j in range(0, self.sizeMatrix):
                if self.board[i][j] == self.EMPTY:
                    self.board[i][j] = self.X
                    (m, min_i, in_j) = self.min_alpha_beta(alpha, beta)
                    if m > max_v:
                        max_v = m
                        px = i
                        py = j
                    self.board[i][j] = self.EMPTY

                    if max_v >= beta:
                        return (max_v, px, py)
                    if max_v > alpha:
                        alpha = max_v


                

sessionPlay = CaroGame()
sessionPlay.board = [
    [X, O, X, O, X, O],
    [O, X, O, X, O, X],
    [X, O, X, O, X, O],
    [O, X, O, X, O, X],
    [X, O, X, O, X, O],
    [O, X, O, X, O, X],
]
print(sessionPlay.winner(sessionPlay.board))
