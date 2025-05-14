from enum import Enum


class Cell(Enum):
    X = "X"
    O = "O"
    NONE = None

    def toInt(self) -> int:
        return 0 if self == Cell.NONE else 1 if self == Cell.X else 2
