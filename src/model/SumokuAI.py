from util.cell import Cell
from util.point import Point
from model.Heuristic import Heuristic
from model.CaroModel import CaroModel
import random

from util.zobrist import ZobristTable

class SumokuAI(CaroModel):
    def __init__(self):
        super().__init__()
        self.heuristic = Heuristic()
        self.MAX_DEPTH = 3
        self.opponent_player = {Cell.X: Cell.O, Cell.O: Cell.X}
        self.empty_cells = 0
        self.transposition_table = {}
        self._heuristic_cache = {}  # Cache for heuristic evaluations
        self._optimal_list_cache = {}  # Cache for optimal lists

    def predict_move(self, board, symbol):
        point: Point = None
        best_move = self.alpha_beta(board, symbol)

        if best_move:
            y, x = best_move
            point = Point(x, y)
            return point
            
        return None

    def alpha_beta(self, board, player) -> Point | None:
        self.heuristic.evaluate_each_cell(board, player)
        ls = self.heuristic.get_optimal_list()
        _max = float('-inf')
        ls_choose = []

        for y, x in ls:
            self.make_move(board, y, x, player)

            _value = self.min_value(board, float('-inf'), float('inf'), 0, self.opponent_player[player], 0, (y, x))

            if _max < _value:
                _max = _value
                ls_choose.clear()
                ls_choose.append((y, x))
            elif _max == _value:
                ls_choose.append((y, x))

            self.undo_move(board, y, x)

        return random.choice(ls_choose)

    def min_value(self, board, alpha, beta, depth, player, hashed_board, last_move):
        if depth >= self.MAX_DEPTH or self.check_winner(board, player, last_move) or self.is_over():
            return self.heuristic.evaluate_board(board)
        
        # Check transposition table
        cached_value = self.zobrist.get_cache(hashed_board, last_move[1], last_move[0], player)
        if cached_value is not None:
            return cached_value

        self.heuristic.evaluate_each_cell(board, player)
        ls = self.heuristic.get_optimal_list()
        value = float('inf')

        for y, x in ls:
            self.make_move(board, y, x, self.opponent_player[player])
            value = min(value, self.max_value(board, alpha, beta, depth + 1, self.opponent_player[player], hashed_board, (y, x)))
            beta = min(beta, value)
            self.undo_move(board, y, x)

            if alpha >= beta:
                break

        # Store in transposition table
        self.zobrist.lets_cache(hashed_board, last_move[1], last_move[0], player, value)
        return value

    def max_value(self, board, alpha, beta, depth, player, hashed_board, last_move) -> float:
        if depth >= self.MAX_DEPTH or self.check_winner(board, player, last_move) or self.is_over():
            return self.heuristic.evaluate_board(board)

        # Check transposition table
        cached_value = self.zobrist.get_cache(hashed_board, last_move[1], last_move[0], player)
        if cached_value is not None:
            return cached_value

        self.heuristic.evaluate_each_cell(board, player)
        ls = self.heuristic.get_optimal_list()
        value = float('-inf')

        for y, x in ls:
            self.make_move(board, y, x, player)
            value = max(value, self.min_value(board, alpha, beta, depth + 1, self.opponent_player[player], hashed_board, (y, x)))
            alpha = max(alpha, value)
            self.undo_move(board, y, x)

            if alpha >= beta:
                break

        # Store in transposition table
        self.zobrist.lets_cache(hashed_board, last_move[1], last_move[0], player, value)
        return value
