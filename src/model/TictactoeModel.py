from typing import List

from util.cell import Cell


class TictactoeModel:
    def __init__(self):
        pass

    def checkWinner(self, board: List[List[Cell]]):
        for i in range(3):
            if (
                board[i][0] == board[i][1]
                and board[i][1] == board[i][2]
                and board[i][0] != Cell.NONE
            ):
                return board[i][0]

            if (
                board[0][i] == board[1][i]
                and board[1][i] == board[2][i]
                and board[0][i] != Cell.NONE
            ):
                return board[0][i]

        if (
            board[0][0] == board[1][1]
            and board[1][1] == board[2][2]
            and board[0][0] != Cell.NONE
        ):
            return board[0][0]

        if (
            board[0][2] == board[1][1]
            and board[1][1] == board[2][0]
            and board[0][2] != Cell.NONE
        ):
            return board[0][2]

        return None

    def terminal(self, board: List[List[Cell]]):
        if self.checkWinner(board) is not None:
            return True

        for i in range(3):
            for j in range(3):
                if board[i][j] == Cell.NONE:
                    return False
        return True

    def player(self, board: List[List[Cell]]) -> Cell:
        x_count = 0
        o_count = 0

        for i in range(3):
            for j in range(3):
                if board[i][j] == Cell.X:
                    x_count += 1
                elif board[i][j] == Cell.O:
                    o_count += 1

        if x_count > o_count:
            return Cell.O
        else:
            return Cell.X

    def result(self, board: List[List[Cell]], action, symbol: Cell):
        new_board = [[board[i][j] for j in range(3)] for i in range(3)]

        new_board[action[0]][action[1]] = symbol

        return new_board

    def min_alpha_beta(self, alpha: int, beta: int, board: List[List[Cell]]):
        minv = 2
        qx = None
        qy = None

        result = self.terminal(board)
        if result is True:
            winner_person = self.checkWinner(board)
            if winner_person == Cell.X:
                return (1, 0, 0)
            elif winner_person == Cell.O:
                return (-1, 0, 0)
            else:
                return (0, 0, 0)

        for action in self.actions(board):
            (i, j) = action
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

    def actions(self, board: List[List[Cell]]):
        actions = []
        for i in range(3):
            for j in range(3):
                if board[i][j] == Cell.NONE:
                    actions.append((i, j))
        return actions

    def max_alpha_beta(self, alpha: int, beta: int, board: List[List[Cell]]):
        maxv = -2
        px = None
        py = None

        result = self.terminal(board)
        if result is True:
            winner_person = self.checkWinner(board)
            if winner_person == Cell.X:
                return (1, 0, 0)
            elif winner_person == Cell.O:
                return (-1, 0, 0)
            else:
                return (0, 0, 0)

        for action in self.actions(board):
            (i, j) = action
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
