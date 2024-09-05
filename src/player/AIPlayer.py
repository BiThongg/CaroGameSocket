from src.model.CaroModel import CaroModel
from src.player.Player import Player
from src.util.point import Point
from src.util.cell import Cell


class AIPlayer(Player):
    def __init__(self):
        super().__init__()
        self.caroModel = CaroModel()
        return

    def makeMove(self):
        if self.symbol == Cell.X:
            (_, y, x) = self.caroModel.min_alpha_beta(-2, 2, self.game.board)
            super().move(Point(x, y))
            print("AI move: ", x, y)
        else:
            (_, y, x) = self.caroModel.max_alpha_beta(-2, 2, self.game.board)
            super().move(Point(x, y))
