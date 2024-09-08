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


class Room:
    def __init__(self, name, owner: User):
        self.id: str = str(uuid.uuid4())
        self.name: str = name
        self.competitor: User
        self.owner: User = owner
        self.guests: List[User] = []
        self.game: Game

    def kick(self, userId: str):
        requestId = request.sid
        if requestId != self.owner.id:
            raise Exception("You are not the owner")

        if self.competitor is not None and self.competitor.id == userId:
            self.competitor = None

        else:
            for user in self.guests:
                if user.id == userId:
                    self.guests.remove(user)
                    break

    def addGuest(self, user: User):
        self.guests.append(user)

    def addCompetitor(self, user: User):
        self.competitor = user

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
