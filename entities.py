import uuid
import numpy as np
from datetime import datetime

class User():
    def __init__(self, id, name):
        self.id = str(id)
        self.name = name
        self.room_played = []
        self.latest_room = None # In case until in game play if guest/lead suddenly out game, we can rely on this value to continue game

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
        else:
            self.watchers.remove(id)
        self.ready_player.remove(id)

    def isInRoom(self, id):
        return self.lead == id or self.guest == id

    def isReady(self):
        return len(self.ready_player) == 2

    def isFull(self):
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
    
    # def get_players_nbr(self):
    #     return len(self.onlineClients)

    # def check_players_game_start(self):
    #     for player in self.onlineClients:
    #         if player.get_game_intention() == False:
    #             self.gameRound = False
    #             return
    #         self.gameRound = True

    # def get_rand_active_player(self):
    #     self.activePlayer = randint(0, 1)
    #     return self.activePlayer

    # def get_swap_player(self):
    #     self.activePlayer =  int(not(bool(self.activePlayer)))
    #     return self.activePlayer

    # def get_ready_for_game(self):
    #     self.check_players_game_start()
    #     return self.gameRound

    # def roomAvailable(self):
    #     """
    #     check to have only 2 players joined
    #     """
    #     if len(self.onlineClients) < 2:
    #         return True
    #     else:
    #         return False

    # def getPlayerIdx(self, sid):
    #     """
    #     return the player index from active game room
    #     Arguments:
    #     sid: id 
    #     """
    #     idx = 0
    #     for player in self.onlineClients:
    #         if player.id == sid:
    #             return idx
    #         idx +=1
    
    # def getClientsInRoom(self, requestType = 'byID'):
    #     connectedPlayers = []

    #     for player in self.onlineClients:
    #         if requestType == 'byId':
    #             connectedPlayers.append(player.id)
    #         elif requestType == 'byName':
    #             connectedPlayers.append(player.name)
    #     return connectedPlayers

    # def startRound(self):
    #     for player in self.onlineClients:
    #         player.gameStartIntention = False
