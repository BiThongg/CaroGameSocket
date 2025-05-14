from abc import ABC, abstractmethod
from util.cell import Cell
from util.point import Point
from model.Heuristic import Heuristic
import random
from util.zobrist import ZobristTable
import numpy as np

class CaroModel(ABC):
    def __init__(self):
        self.empty_cells = 0
        self.current_hash = 0
        self._board_size = None
        self._directions = np.array([
            [1, 0],   # vertical
            [0, 1],   # horizontal
            [1, 1],   # main diagonal
            [-1, 1]   # anti diagonal
        ])

    @abstractmethod
    def predict_move(self, board, symbol) -> Point | None:
        pass
    
    def init_game(self, board):
        self.empty_cells = sum(row.count(Cell.NONE) for row in board)
        self._board_size = len(board)

    def is_over(self):
        return self.empty_cells == 0

    def check_winner(self, board, player, last_move, streak = 5) -> bool:
        y, x = last_move
        
        # Convert board to numpy array for faster operations
        board_array = np.array(board)
        
        # Check each direction
        for dy, dx in self._directions:
            count = 1
            
            # Forward check
            ny, nx = y + dy, x + dx
            while (0 <= ny < self._board_size and 
                   0 <= nx < self._board_size and 
                   board_array[ny, nx] == player):
                count += 1
                ny += dy
                nx += dx
            
            # Backward check
            ny, nx = y - dy, x - dx
            while (0 <= ny < self._board_size and 
                   0 <= nx < self._board_size and 
                   board_array[ny, nx] == player):
                count += 1
                ny -= dy
                nx -= dx
            
            if count >= streak:
                return True
        
        return False

    def make_move(self, board, y, x, player) -> None:
        # Update hash before making the move
        board[y][x] = player
        self.empty_cells -= 1

    def undo_move(self, board, y, x) -> None:
        # Update hash before undoing the move
        board[y][x] = Cell.NONE
        self.empty_cells += 1
