from game.Game import Game
from player.Player import Player
from util.cell import Cell
from random import randint

class CasualGame(Game):
    def __init__(self, size: int = 14):
        super().__init__(size)

    def getWinnerSymbol(self) -> Cell | None:
        # caro _sizex15, 5 for win
        size = self.board.__len__()

        for i in range(size):
            for j in range(size):
                if self.board[i][j] != Cell.NONE:
                    # check horizontal
                    if j < size - 4:
                        if (
                            self.board[i][j]
                            == self.board[i][j + 1]
                            == self.board[i][j + 2]
                            == self.board[i][j + 3]
                            == self.board[i][j + 4]
                        ):
                            return self.board[i][j]
                    # check vertical
                    if i < size - 4:
                        if (
                            self.board[i][j]
                            == self.board[i + 1][j]
                            == self.board[i + 2][j]
                            == self.board[i + 3][j]
                            == self.board[i + 4][j]
                        ):
                            return self.board[i][j]
                    # check diagonal
                    if i < size - 4 and j < size - 4:
                        if (
                            self.board[i][j]
                            == self.board[i + 1][j + 1]
                            == self.board[i + 2][j + 2]
                            == self.board[i + 3][j + 3]
                            == self.board[i + 4][j + 4]
                        ):
                            return self.board[i][j]
                    if i < size - 4 and j > 4:
                        if (
                            self.board[i][j]
                            == self.board[i + 1][j - 1]
                            == self.board[i + 2][j - 2]
                            == self.board[i + 3][j - 3]
                            == self.board[i + 4][j - 4]
                        ):
                            return self.board[i][j]
        return None

    def getWinner(self) -> Player | None:
        symbol = self.getWinnerSymbol()
        for player in self.players:
            if player.symbol == symbol:
                return player
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
