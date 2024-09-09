from typing import Dict, List
import uuid

from flask import request

from game.Game import Game
from game.TicTacToe import TicTacToe
from game.CasualGame import CasualGame
from User import User
from player.AIPlayer import AIPlayer
from player.PersonPlayer import PersonPlayer
from player.Player import Player
from enum import Enum

class Status(Enum): # use enum i cant serialize
    WAITING = "WAITING"
    READY = "READY"

class Participant: 
    def __init__(self, user: User):
        self.info: User = user
        self.status: bool = False

class Room:
    def __init__(self, name, owner: User):
        self.id: str = str(uuid.uuid4())
        self.name: str = name
        self.competitor: Participant = None
        self.owner: Participant = Participant(owner)
        
        self.guests: List[User] = []
        self.game: Game

    def kick(self, userId: str):
        requestId = request.sid
        if requestId != self.owner.info.id:
            raise Exception("You are not the owner")

        if self.competitor is not None and self.competitor.info.id == userId:
            self.competitor = None

        else:
            for user in self.guests:
                if user.id == userId:
                    self.guests.remove(user)
                    break

    def addGuest(self, user: User):
        self.guests.append(user)

    def addCompetitor(self, user: User):            
        self.competitor = Participant(user)
        if user.id.startswith("BOT_"):
            self.competitor.status = True

    def addGame(self, game: Game):
        self.game = game
        player1: Player = PersonPlayer(self.owner)
        player2: Player 

        if(self.competitor.id == "bot"): 
            player2 = AIPlayer(self.competitor)
        else: 
            player2 = PersonPlayer(self.competitor)
        
        self.game.addPlayer(player1)
        self.game.addPlayer(player2)
        

    def getOwner(self) -> User:
        return self.owner

    def onLeave(self, userId: str) -> None:
        if userId == self.owner.id:
            self.owner = self.competitor
            self.competitor = None
        elif userId == self.competitor.id:
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
        self.guests[user.id] = user

    def onDispose(self) -> None:
        pass

    def isFull(self) -> bool:
        return self.competitor is not None and self.owner is not None # and len(self.guests) >= 5
    
    def canAction(self, owner) -> bool:
        return owner.id == self.owner.id

    def isReady(self) -> bool:
        return self.competitor.status == Status.READY and self.owner.status == Status.READY 

    def changeStatus(self, userId: str):
        participant: Participant = self.owner if self.owner.info.id == userId else self.competitor
        participant.status = False if participant.status == True else True

    def participantIds(self):
        ids = [watcher.id for watcher in self.guests]
        ids.append(self.owner.info.id)
        if self.competitor is not None:
            ids.append(self.competitor.info.id)
