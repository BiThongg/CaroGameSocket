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


class UserStatus(Enum):
    NOT_READY = "NOT_READY"
    READY = "READY"


class GameType(Enum):
    TIC_TAC_TOE = "TIC_TAC_TOE"
    CASUAL = "CASUAL"


class GameFactory:
    gameDict = {
        GameType.TIC_TAC_TOE: TicTacToe,
        GameType.CASUAL: CasualGame,
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

        self.guests: List[User] = []
        self.game: Game = None

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

    # def changeGameType(self, gameType: str) -> None:
    #     if request.sid != self.owner.info.id:
    #         raise Exception("You are not the owner")
    #     try:
    #         if self.owner.info.id == request.sid:
    #             self.gameType = GameType[gameType]
    #     except KeyError:
    #         raise Exception(f"Not found any game type with {gameType} !")

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
        # game.randomSeed()
        player1.symbol = Cell.X
        player2.symbol = Cell.O
        game.updateTurn()

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
        if self.isFull():
            self.guests.append(user)
            return
        self.addCompetitor(user)

    def onDispose(self) -> None:
        pass

    def isFull(self) -> bool:
        return self.competitor is not None and self.owner is not None

    def canAction(self, owner) -> bool:
        return owner.id == self.owner.id

    def isReady(self) -> bool:
        return (
            self.competitor.status == UserStatus.READY
            and self.owner.status == UserStatus.READY
        )

    def checkConditionForStart(self, user_id) -> bool:
        if not self.isFull():
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
        return [x for x in ids if x is not None]

    def addBot(self) -> None:
        self.competitor = Participant(User("BOT_" + str(uuid.uuid4()), None))
        self.competitor.status = UserStatus.READY
