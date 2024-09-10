from __future__ import annotations
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod
from util.point import Point
from util.cell import Cell
from User import User

if TYPE_CHECKING:
    from game.Game import Game


class Player(ABC):

    def __init__(self, user: User | None = None):
        self.game: Game = None
        self.symbol: Cell = Cell.NONE
        self.user = user

    def move(self, point: Point):
        self.game.handleMove(self, point)
