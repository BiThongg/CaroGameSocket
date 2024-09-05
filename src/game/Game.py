from __future__ import annotations
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod
from src.util.cell import Cell
from src.util.point import Point
from typing import List
import random

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
        if self.turn != player.symbol:
            raise Exception("Not your turn")

        if self.board[point.x][point.y] != Cell.NONE:
            raise Exception("Cell is not empty")

        self.board[point.x][point.y] = player.symbol
        self.updateTurn()
        return

    def addPlayer(self, player: Player) -> None:
        player.game = self
        self.players.append(player)
        return

    def removePlayer(self, player: Player) -> None:
        player.game = None
        self.players.remove(player)
        return

    def isGameOver(self) -> bool:
        if (self.getWinner()) is not None:
            return True
        return False

    def drawBoard(self) -> None:
        for row in self.board:
            for cell in row:
                if cell == Cell.NONE:
                    print(" ", end=" ")
                else:
                    print(cell.value, end=" ")

        print(end="\n")
        return

    @abstractmethod
    def getWinner(self) -> Player:
        pass

    @abstractmethod
    def updateTurn(self) -> None:
        pass

    @abstractmethod
    def randomSeed(self) -> None:
        pass
