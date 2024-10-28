from typing import List
import uuid

from numpy import random
from game.Game import Game
from game.TicTacToe import TicTacToe
from game.CasualGame import CasualGame
from User import User
from player.AIPlayer import AIPlayer
from player.PersonPlayer import PersonPlayer
from player.Player import Player
from enum import Enum
from util.cell import Cell
from typing import Type, Callable, Dict
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.schedulers.background import BackgroundScheduler
from config import socketio

class UserStatus(Enum):
    NOT_READY = "NOT_READY"
    READY = "READY"

class GameType(Enum):
    TIC_TAC_TOE = "TIC_TAC_TOE"
    CASUAL = "CASUAL"

class GameFactory:
    gameDict: Dict[Enum, Type] = {
        GameType.TIC_TAC_TOE: TicTacToe,
        GameType.CASUAL: CasualGame
    }

    @staticmethod
    def construct(gameType: GameType) -> Game:
        return GameFactory.gameDict[gameType]()

class Participant:
    def __init__(self, user: User):
        self.info: User = user
        self.status: UserStatus = UserStatus.READY

class Room:
    def __init__(self, name, owner: User):
        self.id: str = str(random.randint(100000, 100000 * 2 - 1))
        self.name: str = name
        self.competitor: Participant = None
        self.owner: Participant = Participant(owner)
        self.gameType: GameType = GameType.CASUAL
        self._scheduler: BackgroundScheduler = BackgroundScheduler()
        self.guests: List[User] = []
        self.game: Game = None
        self.onRoomTimer()
        
    # -> Destroy timer
    # desc: start timer khi vừa tạo phòng, 
    # interval mỗi 15s 1 lần {nếu ko có game và chưa đủ player thì xóa room}. 
    # Khi vừa hết game thì restart room's timer
    def onRoomTimer(self):
        self.startTimer()

    def startTimer(self): # Waiting time for room was being fixed 15s
        self._scheduler.add_job(
            self.timeout,
            "interval",
            seconds=15,
            id="room_waiting_time",
            replace_existing=True
        )
        self._scheduler.start()
        
    def restartTimer(self):
        try:
            self._scheduler.reschedule_job(job_id="room_waiting_time", trigger=IntervalTrigger(seconds=15))
        except Exception as e:
            print(f"Failed to modify job {'player_turn_timer'}: {e}")

    def timeout(self):
        if not self.isFullPlayer() and self.game is None:
            self._scheduler.remove_all_jobs()
            socketio.emit("room_destroyed", {
                "message": "The room was canceled due to timeout !"
            }, to=self.participantIds())
        else:
            try:
                self._scheduler.reschedule_job(job_id="room_waiting_time", trigger=IntervalTrigger(seconds=15))
            except Exception as e:
                print(f"Failed to modify job {'player_turn_timer'}: {e}")
    # End timer

    def kick(self, owner_id: str, kickId: str) -> str:
        if owner_id != self.owner.info.id:
            raise Exception("You are not owner")

        sid = None

        if self.competitor is not None and self.competitor.info.id == kickId:
            sid = self.competitor.info.sid
            self.competitor = None
        else:
            for user in self.guests:
                if user.id == kickId:
                    sid = user.sid
                    self.guests.remove(user)
                    break
        return sid
    def addGuest(self, user: User):
        self.guests.append(user)
    

    def addCompetitor(self, user: User):
        self.competitor = Participant(user)

    def gameStart(self, gameType: str):
        player1: Player = PersonPlayer(self.owner.info)
        player2: Player = (
            AIPlayer(self.competitor.info)
            if self.competitor.info.name.startswith("BOT_")
            else PersonPlayer(self.competitor.info)
        )

        game: Game = GameFactory.construct(GameType[gameType])
        game.addPlayer(player1)
        game.addPlayer(player2)
        self.game = game
        game.room = self
        
        player1.symbol = Cell.X
        player2.symbol = Cell.O

    def getOwnerInfo(self) -> User:
        return self.owner.info

    def onLeave(self, userId: str) -> None:
        if userId == self.owner.info.id:
            self.owner = self.competitor
            self.competitor = None

        elif userId == self.competitor.info.id:
            self.competitor = None
        else:
            userTmp = None
            for user in self.guests:
                if user.id == userId:
                    userTmp = user
                    break
            if userTmp is not None:
                self.guests.remove(userTmp)


    def onJoin(self, user: User) -> None:
        if self.isFullPlayer():
            self.guests.append(user)
        else:
            self.addCompetitor(user)

    def onDispose(self) -> None:
        self._scheduler.shutdown()

    def isFullPlayer(self) -> bool:
        return self.competitor is not None and self.owner is not None

    def canAction(self, owner) -> bool:
        return owner.id == self.owner.id

    def isReady(self) -> bool:
        return (
            self.competitor.status == UserStatus.READY
            and self.owner.status == UserStatus.READY
        )

    def checkConditionForStart(self, user_id) -> bool:
        if not self.isFullPlayer():
            return False

        if user_id != self.owner.info.id or not self.isReady():
            return False
        
        return True

    def changeStatus(self, userId: str):
        participant: Participant = (
            self.owner if self.owner.info.id == userId else self.competitor
        )
        participant.status = (
            UserStatus.NOT_READY
            if (participant.status == UserStatus.READY)
            else UserStatus.READY
        )

    def participantIds(self) -> list[str]:
        ids = [watcher.sid for watcher in self.guests]
        ids.append(self.owner.info.sid)
        if self.competitor is not None:
            ids.append(self.competitor.info.sid)
        return [x for x in ids if x is not None and not x.startswith('BOT_')]

    def addBot(self) -> None:
        self.competitor = Participant(User("BOT_" + str(uuid.uuid4()), None))
        self.competitor.status = UserStatus.READY
