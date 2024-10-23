from User import User
from model.TictactoeModel import TictactoeModel
from model.SumokuModel import CaroModel
from player.Player import Player
from util.point import Point
from util.cell import Cell
from game.CasualGame import *
from game.TicTacToe import *
from typing import Type, Callable, Dict


class AIPlayer(Player):
    def __init__(self, user: User | None):
        super().__init__(user)
        self.caroModel = CaroModel()
        self.tictactoeModel = TictactoeModel()

    def makeMoveFactory(self) -> Callable[[], str]:
        makeMoveFactory: Dict[Type, Callable[[], str]] = {
            CasualGame.__name__: self.makeMoveSumoku,
            TicTacToe.__name__: self.makeMoveTictactoe,
        }
        return makeMoveFactory[self.game.__class__.__name__]

    def makeMove(self):
        self.makeMoveFactory()()

    def makeMoveSumoku(self):
        board = self.deepCopyBoard(self.game.board)
        point: Point = None
        if self.symbol == Cell.X:
            (a, y, x) = self.caroModel.max_alpha_beta(-2, 2, board)
            point = Point(x, y)
            super().move(point)
        else:
            (a, y, x) = self.caroModel.min_alpha_beta(-2, 2, board)
            point = Point(x, y)
            super().move(point)

        self.game.latestPoint = point

    def makeMoveTictactoe(self):
        board = self.deepCopyBoard(self.game.board)
        point: Point = None
        if self.symbol == Cell.X:
            (a, y, x) = self.tictactoeModel.max_alpha_beta(-2, 2, board)
            point = Point(x, y)
            super().move(point)
        else:
            (a, y, x) = self.tictactoeModel.min_alpha_beta(-2, 2, board)
            point = Point(x, y)
            super().move(point)
        self.game.latestPoint = point

    def deepCopyBoard(self, board):
        return [row[:] for row in board]
