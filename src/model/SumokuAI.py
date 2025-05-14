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
        self.MAX_DEPTH = 5
        self.opponent_player = {Cell.X: Cell.O, Cell.O: Cell.X}
        self.empty_cells = 0
        self.zobrist = ZobristTable(14, 14, 3)
        self.transposition_table = {}
        self._heuristic_cache = {}  # Cache for heuristic evaluations
        self._optimal_list_cache = {}  # Cache for optimal lists

    def _get_board_key(self, board):
        # Create a unique key for the board state
        return hash(tuple(tuple(row) for row in board))

    def _get_cached_heuristic(self, board, player):
        board_key = self._get_board_key(board)
        cache_key = (board_key, player)
        
        if cache_key in self._heuristic_cache:
            return self._heuristic_cache[cache_key]
            
        self.heuristic.evaluate_each_cell(board, player)
        value = self.heuristic.evaluate_board(board)
        self._heuristic_cache[cache_key] = value
        return value

    def _get_cached_optimal_list(self, board, player):
        board_key = self._get_board_key(board)
        cache_key = (board_key, player)
        
        if cache_key in self._optimal_list_cache:
            return self._optimal_list_cache[cache_key]
            
        self.heuristic.evaluate_each_cell(board, player)
        optimal_list = self.heuristic.get_optimal_list()
        self._optimal_list_cache[cache_key] = optimal_list
        return optimal_list

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

            _value = self.min_value(board, float('-inf'), float('inf'), 0, player, (y, x))

            if _max < _value:
                _max = _value
                ls_choose.clear()
                ls_choose.append((y, x))
            elif _max == _value:
                ls_choose.append((y, x))

            self.undo_move(board, y, x)

        return random.choice(ls_choose)

    def min_value(self, board, alpha, beta, depth, player, last_move) -> float:
        if depth >= self.MAX_DEPTH or self.check_winner(board, player, last_move) or self.is_over():
            return self._get_cached_heuristic(board, player)

        # Check transposition table
        cached_value = self.zobrist.get_cache(last_move[1], last_move[0], player)
        if cached_value is not None:
            return cached_value

        ls = self._get_cached_optimal_list(board, player)
        value = float('inf')

        for y, x in ls:
            self.make_move(board, y, x, player)
            value = min(value, self.max_value(board, alpha, beta, depth + 1, player, (y, x)))
            beta = min(beta, value)
            self.undo_move(board, y, x)

            if alpha >= beta:
                break

        # Store in transposition table
        self.zobrist.lets_cache(last_move[1], last_move[0], player, value)
        return value

    def max_value(self, board, alpha, beta, depth, player, last_move) -> float:
        if depth >= self.MAX_DEPTH or self.check_winner(board, player, last_move) or self.is_over():
            return self._get_cached_heuristic(board, player)

        # Check transposition table
        cached_value = self.zobrist.get_cache(last_move[1], last_move[0], player)
        if cached_value is not None:
            return cached_value

        ls = self._get_cached_optimal_list(board, player)
        value = float('-inf')

        for y, x in ls:
            self.make_move(board, y, x, player)
            value = max(value, self.min_value(board, alpha, beta, depth + 1, player, (y, x)))
            alpha = max(alpha, value)
            self.undo_move(board, y, x)

            if alpha >= beta:
                break

        # Store in transposition table
        self.zobrist.lets_cache(last_move[1], last_move[0], player, value)
        return value
