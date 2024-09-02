import uuid
import numpy as np
from datetime import datetime

class User():
    def __init__(self, id, name):
        self.id = str(id)
        self.name = name
        # self.room_played = []
        # self.latest_room = None # In case until in game play if guest/lead suddenly out game, we can rely on this value to continue game

class Room():
    def __init__(self, name):
        self.id = str(uuid.uuid4())
        self.name = name
        self.lead = None
        self.guest = None
        self.status = None
        self.ready_player = []
        self.game = []
        self.watchers = []
    
    def leave_room(self, id):
        if self.lead == id:
            self.lead = None
            if self.guest != None:
                self.lead = self.guest
                self.guest = None
        elif self.guest == id:
            self.guest = None
        elif id in self.watchers:
            self.watchers.remove(id)
        if id in self.ready_player:
            self.ready_player.remove(id)

    def is_in_room(self, id):
        return self.lead == id or self.guest == id or id in self.watchers

    def is_ready(self):
        return len(self.ready_player) == 2

    def is_full(self):
        return self.lead != None and self.guest != None

class Game():
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.winner = None
        self.room = None
        self.start_at = datetime.now()
        self.chessboard = np.zeros((15, 15))

    def add_player(self, objPlayer):
        self.onlineClients.append(objPlayer)