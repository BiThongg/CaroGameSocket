from typing import List
import uuid

from src.game import Game
from src.User import User


class Room:
    def __init__(self, name, owner: User):
        self.id: str = str(uuid.uuid4())
        self.name: str = name
        # self.users:List[User] = []
        # self.game:Game
        self.owner = owner

    def kick(self, uuid: str):
        self.users.remove(uuid)

    def add_user(self, user: User):
        self.users.append(user.id)

    def add_game(self, game: Game):
        self.game = game

        # self.lead = None
        # self.guest = None
        # self.status = None
        # self.ready_player = []
        # self.game = []
        # self.watchers = []
        # self.users = []

    #
    # def leave_room(self, id):
    #     if self.lead == id:
    #         self.lead = None
    #         if self.guest != None:
    #             self.lead = self.guest
    #             self.guest = None
    #     elif self.guest == id:
    #         self.guest = None
    #     elif id in self.watchers:
    #         self.watchers.remove(id)
    #     if id in self.ready_player:
    #         self.ready_player.remove(id)
    #
    # def is_in_room(self, id):
    #     return self.lead == id or self.guest == id or id in self.watchers
    #
    # def is_ready(self):
    #     return len(self.ready_player) == 2
    #
    # def is_full(self):
    #     return self.lead != None and self.guest != None
