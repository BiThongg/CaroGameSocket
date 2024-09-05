from abc import ABC, abstractmethod

from game import Game
from point import Point


class Player(ABC):
    game = None 

    def __init__(self, symbol):
        self.symbol = symbol
        return

    def move(self, point: Point):
        if self.game == None:
            raise Exception("Game is not set")

        if self.game.board[point.y][point.x] is not None:
            raise Exception("Invalid move")
        else:
            self.game.board[point.y][point.x] = self.symbol
            # tuirn is true or false 
            self.game.turn = not self.game.turn
            return True
