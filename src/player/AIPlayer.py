from src.model.TictactoeModel import TictactoeModel
from src.model.CaroModel import CaroModel
from src.player.Player import Player
from src.util.point import Point
from src.util.cell import Cell


class AIPlayer(Player):
    def __init__(self):
        super().__init__()
        self.caroModel = CaroModel()
        self.tictactoeModel = TictactoeModel()
        return

    def makeMoveSumoku(self):
        if self.symbol == Cell.X:
            (_, y, x) = self.caroModel.min_alpha_beta(-2, 2, self.game.board)
            super().move(Point(x, y))
            print("AI move: ", x, y)
        else:
            (_, y, x) = self.caroModel.max_alpha_beta(-2, 2, self.game.board)
            super().move(Point(x, y))
            print("AI move: ", x, y)

    def makeMoveTictactoe(self):
        if self.symbol == Cell.X:
            (a, y, x) = self.tictactoeModel.max_alpha_beta(-1, 2, self.game.board)
            print("AI move: ", a, x, y)
            super().move(Point(x, y))
            print (self.game.board)
        else:
            (a, y, x) = self.tictactoeModel.min_alpha_beta(-2, 2, self.game.board)
            print("AI move: ", a, x, y)
            super().move(Point(x, y))
            print(self.game.board)
