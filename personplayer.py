from game import Game
from player import Player
from point import Point

class PersonPlayer(Player):
    def __init__(self, symbol, user):
        super().__init__(symbol)
        self.user = user
        return

    def move(self, point: Point):
        super().move(point)
        # sucessMove =  super().move(point)
        # return sucessMove
