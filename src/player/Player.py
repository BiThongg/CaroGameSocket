from __future__ import annotations
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod
from src.util.point import Point
from src.util.cell import Cell
from src.User import User

if TYPE_CHECKING:
    from src.game.Game import Game


class Player(ABC):

    def __init__(self, user: User | None = None):
        self.game: Game = None
        self.symbol: Cell = Cell.NONE
        self.user = user

    def move(self, point: Point):
        self.game.handleMove(self, point)
