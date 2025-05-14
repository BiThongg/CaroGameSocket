from game.Game import Game
from player.Player import Player
from util.cell import Cell
from random import randint
from util.point import Point

# TicTacToe game is who get 3 in a row will win
class TicTacToe(Game):
    targetCount = 3
    
    @staticmethod
    def getClassName() -> str:
        return TicTacToe.__name__

    def __init__(self):
        super().__init__(3)

    def getGameEndInfo(self) -> dict | None:
        result: dict = self.isEndGame()
        if result is not None:
            for player in self.players:
                if player.symbol.name == result['symbol']:
                    return result
        return None

    def updateTurn(self) -> None:
        if self.turn == Cell.X:
            self.turn = Cell.O
        else:
            self.turn = Cell.X
        return

    def randomSeed(self) -> None:
        seed1 = randint(0, 1)
        if seed1 == 0:
            self.players[0].symbol = Cell.X
            self.players[1].symbol = Cell.O
        else:
            self.players[0].symbol = Cell.O
            self.players[1].symbol = Cell.X

        seed2 = randint(0, 1)
        if seed2 == 0:
            self.turn = Cell.X
        else:
            self.turn = Cell.O
