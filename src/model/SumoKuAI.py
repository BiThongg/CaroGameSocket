from util.cell import Cell
from util.point import Point
from model.Heuristic import Heuristic
import random

class SumokuAI:
    def __init__(self):
        self.heuristic = Heuristic()
        self.MAX_DEPTH = 5
        self.opponent_player = {Cell.X: Cell.O, Cell.O: Cell.X}
        self.empty_cells = 0

    def predict_move(self, board, symbol):
        point: Point = None

        best_move = self.alpha_beta(board, symbol)

        if best_move:
            y, x = best_move
            point = Point(x, y)
            return point
            
        return None

    def set_board(self, board):
        self.empty_cells = sum(row.count(Cell.NONE) for row in board)

    def alpha_beta(self, board, player):
        self.heuristic.evaluate_each_cell(board, player)
        ls = self.heuristic.get_optimal_list()
        _max = float('-inf')
        ls_choose = []

        for y, x in ls:
            self.make_move(board, y, x, player)

            _value = self.min_value(board, float('-inf'), float('inf'), 0, self.opponent_player[player], (y, x))

            if _max < _value:
                _max = _value
                ls_choose.clear()
                ls_choose.append((y, x))
            elif _max == _value:
                ls_choose.append((y, x))

            self.undo_move(board, y, x)

        return random.choice(ls_choose)

    def min_value(self, board, alpha, beta, depth, player, last_move):
        if depth >= self.MAX_DEPTH or self.check_winner(board, self.opponent_player[player], last_move) or self.is_over():
            return self.heuristic.evaluate_board(board)

        self.heuristic.evaluate_each_cell(board, self.opponent_player[player])
        ls = self.heuristic.get_optimal_list()

        for y, x in ls:
            self.make_move(board, y, x, self.opponent_player[player])

            beta = min(beta, self.max_value(board, alpha, beta, depth + 1, player, (y, x)))

            self.undo_move(board, y, x)

            if alpha >= beta:
                break
        return beta

    def max_value(self, board, alpha, beta, depth, player, last_move):
        if depth >= self.MAX_DEPTH or self.check_winner(board, player, last_move) or self.is_over():
            return self.heuristic.evaluate_board(board)

        self.heuristic.evaluate_each_cell(board, player)
        ls = self.heuristic.get_optimal_list()

        for y, x in ls:
            self.make_move(board, y, x, player)

            alpha = max(alpha, self.min_value(board, alpha, beta, depth + 1, self.opponent_player[player], (y, x)))

            self.undo_move(board, y, x)

            if alpha >= beta:
                break
        return alpha

    def is_over(self):
        return self.empty_cells == 0

    # Optimization: Check win condition using only the last move
    def check_winner(self, board, player, last_move):
        y, x = last_move
        size = len(board)
        directions = [(1, 0), (0, 1), (1, 1), (-1, 1)]  # vertical, horizontal, main diag, anti diag

        for dy, dx in directions:
            count = 1

            # Check forward
            ny, nx = y + dy, x + dx
            while 0 <= ny < size and 0 <= nx < size and board[ny][nx] == player:
                count += 1
                ny += dy
                nx += dx

            # Check backward
            ny, nx = y - dy, x - dx
            while 0 <= ny < size and 0 <= nx < size and board[ny][nx] == player:
                count += 1
                ny -= dy
                nx -= dx

            if count >= 5:
                return True

        return False

    def make_move(self, board, y, x, player):
        board[y][x] = player
        self.empty_cells -= 1

    def undo_move(self, board, y, x):
        board[y][x] = Cell.NONE
        self.empty_cells += 1
