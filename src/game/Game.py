from __future__ import annotations
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod
from util.point import Point
from typing import List
from rich.console import Console
from rich.table import Table
from enum import Enum
from util.cell import Cell

if TYPE_CHECKING:
    from src.player.Player import Player

class Game(ABC):
    def __init__(self, size: int):
        self.turn: Cell = Cell.NONE
        self.players: List[Player] = []
        self.board: List[List[Cell]] = [
            [Cell.NONE for _ in range(size)] for _ in range(size)
        ]

    def getCurrentSymbol(self) -> Cell:
        return self.turn

    def getCurrentTurn(self) -> Player:
        for player in self.players:
            if player.symbol == self.turn:
                return player

    def handleMove(self, player: Player, point: Point) -> None:
        print("handleMove")
        print(player)
        print(point)
        # if self.turn != player.symbol:
        #     raise Exception("Not your turn")
        #
        # if self.board[point.y][point.x] != Cell.NONE:
        #     raise Exception("Cell is not empty")
        #
        # self.board[point.y][point.x] = player.symbol
        # self.updateTurn()
        return

    def addPlayer(self: Game, player: Player) -> None:
        player.game = self
        self.players.append(player)

    def removePlayer(self, player: Player) -> None:
        player.game = None
        self.players.remove(player)
        return

    def isGameOver(self) -> bool:
        if (self.getWinner()) is not None:
            return True
        return False

    def drawBoard(self) -> None:
        table = Table(title="GAME SIEU DINH")
        rows = []
        for i, row in enumerate(self.board):
            s = list(map(lambda x: " " if x == Cell.NONE else x.value, row))
            rows.append([str(i)] + s)

        columns = ["Y/X"]
        for i in range(len(self.board[0])):
            columns.append(str(i))

        for column in columns:
            table.add_column(column)

        for row in rows:
            table.add_row(*row, style="bright_green")

        console = Console()
        console.print(table)
        return
    
    def serialization(self):
        tmp = self

    @abstractmethod
    def getWinner(self) -> Player:
        pass

    @abstractmethod
    def updateTurn(self) -> None:
        pass

    @abstractmethod
    def randomSeed(self) -> None:
        pass
