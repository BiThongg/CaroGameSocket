from game.Game import Game
from player.Player import Player
from util.cell import Cell
from random import randint


# TicTacToe game is who get 3 in a row will win
class TicTacToe(Game):

    def __init__(self):
        super().__init__(3)

    def getWinnerSymbol(self) -> Cell:
        # caro 3x3, 3 for win
        size = self.board.__len__()
        # check win tictactoe 
        for i in range(size):
            # check horizontal
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != Cell.NONE:
                return self.board[i][0]
            # check vertical
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != Cell.NONE:
                return self.board[0][i]
        # check diagonal
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != Cell.NONE:
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != Cell.NONE:
            return self.board[0][2]
        return Cell.NONE

    def getGameEndInfo(self) -> Player | None:
        # symbol = self.getWinnerSymbol()
        # for player in self.players:
        #     if player.symbol == symbol:
        #         return player
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
