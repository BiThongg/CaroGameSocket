from __future__ import annotations
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod
from apscheduler.schedulers.background import BackgroundScheduler
from util.point import Point
from typing import List
from rich.console import Console
from rich.table import Table
from util.cell import Cell
from apscheduler.triggers.interval import IntervalTrigger
from config import socketio

if TYPE_CHECKING:
    from src.player.Player import Player
    from src.room.Room import Room


class Game(ABC):
    def __init__(self, size: int):
        self.room: Room = None
        self.timeLeft: int = 30
        self.isEnd: bool = False
        self.turn: Cell = Cell.X
        self.latestPoint: Point = None
        self.players: List[Player] = []
        self._scheduler: BackgroundScheduler = BackgroundScheduler()
        self.board: List[List[Cell]] = [
            [Cell.NONE for _ in range(size)] for _ in range(size)
        ]
        self.onGameTimer()
        
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

            i, j = x + dx, y + dy
            while 0 <= i < len(self.board) and 0 <= j < len(self.board[0]) and self.board[i][j] == currentCell:
                movedPoints.append(Point(j, i))
                count += 1
                i += dx
                j += dy
                
            # check chiều âm
            i, j = x - dx, y - dy
            while 0 <= i < len(self.board) and 0 <= j < len(self.board[0]) and self.board[i][j] == currentCell:
                movedPoints.append(Point(j, i))
                count += 1
                i -= dx
                j -= dy
                
            if count >= self.targetCount:
                movedPoints.append(self.latestPoint)
                return {
                    "symbol": currentCell.name,
                    "points": movedPoints
                }
        return None

    # TIMEOUT MODULE
    def onGameTimer(self):
        self.startTimer()

    def startTimer(self):
        if not self.isEnd:
            self._scheduler.add_job(
                self.timeout,
                "interval",
                seconds=self.timeLeft,
                id="player_turn_timer",
                replace_existing=True,
            )
            self._scheduler.start()

    def timeout(self):
        self._scheduler.remove_all_jobs()
        self.playerLoses(self.getCurrentPlayerTurn())

    def playerLoses(self, loser: Player):
        restPlayers = [player for player in self.players if player != loser]
        self.room.game = None
        socketio.emit(
            "ended_game",
            {"message": f"{restPlayers[0].user.name} ({restPlayers[0].symbol}) wins !"},
            to=self.room.participantIds(),
        )

    def modifyTimer(self):
        try:
            self._scheduler.reschedule_job(
                "player_turn_timer", trigger=IntervalTrigger(seconds=self.timeLeft)
            )
        except Exception as e:
            print(f"Failed to modify job {'player_turn_timer'}: {e}")

    # TIMEOUT MODULE

    def isFullBoard(self) -> bool:
        for row in self.board:
            for cell in row:
                if cell == Cell.NONE:
                    return False
        return True

    def endGame(self) -> None:
        self.isEnd = True
        self.room.game = None
        self._scheduler.remove_all_jobs()
        # self.room.onRoomTimer()

    def getCurrentSymbol(self) -> Cell:
        return self.turn

    def getCurrentPlayerTurn(self) -> Player:
        for player in self.players:
            if player.symbol == self.turn:
                return player

    def handleMove(self, player: Player, point: Point) -> None:
        if self.turn != player.symbol:
            raise Exception("Not your turn")

        if self.board[point.y][point.x] != Cell.NONE:
            raise Exception("Cell is not empty")
        self.latestPoint = point
        self.board[point.y][point.x] = player.symbol
        return

    def checkPlayer(self, user_id: str) -> bool:
        for player in self.players:
            if player.user.id == user_id:
                return True
        return False

    def getPlayer(self, user_id: str) -> Player:
        for player in self.players:
            if player.user.id == user_id:
                return player
        return None

    def getBot(self) -> Player:
        for player in self.players:
            if player.user.name.startswith("BOT_"):
                return player
        return None

    def addPlayer(self: Game, player: Player) -> None:
        player.game = self
        self.players.append(player)
        player.init_game()

    def removePlayer(self, player: Player) -> None:
        player.game = None
        self.players.remove(player)
        return

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
    def getGameEndInfo(self) -> Player:
        pass

    @abstractmethod
    def updateTurn(self) -> None:
        pass

    @abstractmethod
    def randomSeed(self) -> None:
        pass

    @staticmethod
    @abstractmethod
    def getClassName() -> str:
        pass
