from typing import List
from caromodel import EMPTY, CaroGame
from game import Game
from player import Player


class SumokuGame(Game):
    def __init__(self, players: List[Player], size: int):
        self.players = players
        self.turn = True 
        self.board = [[EMPTY for _ in range(size)] for _ in range(size)]
        self.caroModel = CaroGame()

        for player in self.players:
            player.game = self
        return

    def getWhoseTurn(self):
        playerX = None
        playerO = None
        if self.players[0].symbol == "X":
            playerX = self.players[0]
            playerO = self.players[1]
        else:
            playerX = self.players[1]
            playerO = self.players[0]

        if self.turn is True:
            return playerX
        else:
            return playerO

    def getWinner(self):
        playerX = None
        playerO = None
        if self.players[0].symbol == "X":
            playerX = self.players[0]
            playerO = self.players[1]
        else:
            playerX = self.players[1]
            playerO = self.players[0]

        symbol = self.caroModel.winner(self.board)

        if symbol == playerX.symbol:
            return playerX
        elif symbol == playerO.symbol:
            return playerO
        else:
            return None

    def drawBoard(self):
        for row in self.board:
            print(row, end="\n")

        print(end="\n")
        return
