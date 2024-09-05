from caromodel import CaroGame
from game import Game
from player import Player
from point import Point

class AIPlayer(Player):
    def __init__(self, symbol):
        super().__init__(symbol)
        return

    def makeMove(self):
        caroGame = CaroGame()
        if self.symbol == CaroGame.X:
            (_, y, x) = caroGame.min_alpha_beta(-2, 2, self.game.board)
            super().move(Point(x, y))
        else:
            (_, y, x) = caroGame.max_alpha_beta(-2, 2, self.game.board)
            super().move(Point(x, y))
