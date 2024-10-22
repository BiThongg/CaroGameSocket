from game.Game import Game
from player.Player import Player
from util.cell import Cell
from random import randint
from util.point import Point

class CasualGame(Game):
    def __init__(self, size: int = 14):
        super().__init__(size)

    def isEndGame(self) -> dict | None:
        currentCell: Cell = self.turn
        x = self.latestPoint.y
        y = self.latestPoint.x

        directions = [
            (1, 0),   # ngang
            (0, 1),   # dọc
            (1, 1),   # chéo chính
            (1, -1)   # chèo phụ
        ]
        
        for dx, dy in directions:
            count = 1
            movedPoints: list[Point] = []
            # check chiều dương
            i, j = x + dx, y + dy
            while 0 <= i < len(self.board) and 0 <= j < len(self.board[0]) and self.board[i][j] == currentCell:
                movedPoints.append(Point(i, j))
                count += 1
                i += dx
                j += dy
                
            # check chiều âm
            i, j = x - dx, y - dy
            while 0 <= i < len(self.board) and 0 <= j < len(self.board[0]) and self.board[i][j] == currentCell:
                movedPoints.append(Point(i, j))
                count += 1
                i -= dx
                j -= dy
                
            if count >= 5: # 5 là caro
                return {
                    "symbol": currentCell,
                    "points": movedPoints
                }
        return None
        
    def getGameEndInfo(self) -> dict | None:
        result: dict = self.isEndGame()
        if result is not None:
            for player in self.players:
                if player.symbol == result['symbol']:
                    result['player'] = player
                    del result['symbol']
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
