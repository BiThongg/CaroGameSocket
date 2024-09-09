from User import User
from model.TictactoeModel import TictactoeModel
from model.SumokuModel import CaroModel
from player.Player import Player
from util.point import Point
from util.cell import Cell


class AIPlayer(Player):
    def __init__(self, user: User | None):
        super().__init__(user)
        self.caroModel = CaroModel()
        self.tictactoeModel = TictactoeModel()
        return

    def makeMoveSumoku(self):
        if self.symbol == Cell.X:
            (a, y, x) = self.caroModel.max_alpha_beta(-2, 2, self.game.board)
            super().move(Point(x, y))
            print("AI move: ", a, x, y)
        else:
            (a, y, x) = self.caroModel.min_alpha_beta(-2, 2, self.game.board)
            super().move(Point(x, y))
            print("AI move: ", a, x, y)

    def makeMoveTictactoe(self):
        if self.symbol == Cell.X:
            (a, y, x) = self.tictactoeModel.max_alpha_beta(-2, 2, self.game.board)
            print("AI move: ", a, x, y)
            super().move(Point(x, y))
            print(self.game.board)
        else:
            (a, y, x) = self.tictactoeModel.min_alpha_beta(-2, 2, self.game.board)
            print("AI move: ", a, x, y)
            super().move(Point(x, y))
            print(self.game.board)
