import time
from src.util.cell import Cell


class CaroModel:
    board = []
    start = time.time()

    time_limit = 3

    def __init__(self):
        pass

    def actions(self, board):
        possible_actions = set()

        for i in range(board.__len__()):
            for j in range(board[i].__len__()):
                if board[j][i] == Cell.NONE:
                    possible_actions.add((j, i))

        return possible_actions

    def result(self, board, action):
        if action not in self.actions(board):
            raise Exception("Invalid action")

        new_board = [row[:] for row in board]

        new_board[action[0]][action[1]] = self.player(board)

        return new_board

    def player(self, board):
        """
        Returns player who has the next turn on a board.
        """

        x_count = 0
        o_count = 0

        for i in range(self.sizeMatrix):
            for j in range(self.sizeMatrix):
                if board[j][i] == Cell.X:
                    x_count += 1
                elif board[j][i] == Cell.O:
                    o_count += 1

        if x_count > o_count:
            return Cell.O
        else:
            return Cell.X

    def terminal(self, board):
        if self.winner(board) is not None:
            return True

        for i in range(board.__len__()):
            for j in range(board[i].__len__()):
                if board[j][i] == Cell.NONE:
                    return False

        return True

    def winner(self, board):
        _size = board.__len__()

        for i in range(_size):
            for j in range(_size):
                if board[i][j] != Cell.NONE:
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
        if self.winner(board) == Cell.X:
            return 1
        elif self.winner(board) == Cell.O:
            return -1
        else:
            return 0

    def minimax(self, board):
        if self.terminal(board):
            return self.utility(board)

        if self.player(board) == Cell.X:
            return self.max_alpha_beta(-2, 2)
        return 1

    def max_alpha_beta(self, alpha, beta, board):
        maxv = -2
        px = None
        py = None

        result = self.terminal(board)
        if result is True:
            winner_person = self.winner(board)
            if winner_person == Cell.X:
                return (1, 0, 0)
            elif winner_person == Cell.O:
                return (-1, 0, 0)
            else:
                return (0, 0, 0)

        start = time.time()

        for action in self.actions(board):
            (i, j) = action
            if (time.time() - start) > self.time_limit:
                return (maxv, px, py)
            board[i][j] = Cell.X
            (m, min_i, min_j) = self.min_alpha_beta(alpha, beta, board)
            if m == 1:
                board[i][j] = Cell.NONE
                return (1, i, j)

            if m > maxv:
                maxv = m
                px = i
                py = j
            board[i][j] = Cell.NONE

            if maxv >= beta:
                return (maxv, px, py)

            if maxv > alpha:
                alpha = maxv

        return (maxv, px, py)

    def min_alpha_beta(self, alpha, beta, board):
        minv = 2

        qx = None
        qy = None

        result = self.terminal(board)
        if result is True:
            winner_person = self.winner(board)
            if winner_person == Cell.X:
                return (1, 0, 0)
            elif winner_person == Cell.O:
                return (-1, 0, 0)
            else:
                return (0, 0, 0)
        start = time.time()

        for i in range(0, board.__len__()):
            for j in range(0, board[i].__len__()):
                if (time.time() - start) > self.time_limit:
                    return (minv, qx, qy)

                if board[i][j] == Cell.NONE:
                    board[i][j] = Cell.O
                    (m, max_i, max_j) = self.max_alpha_beta(alpha, beta, board)
                    if m == -1:
                        board[i][j] = Cell.NONE
                        return (-1, i, j)

                    if m < minv:
                        minv = m
                        qx = i
                        qy = j
                    board[i][j] = Cell.NONE

                    if minv <= alpha:
                        return (minv, qx, qy)

                    if minv < beta:
                        beta = minv

        return (minv, qx, qy)
