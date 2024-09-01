import numpy as np

class User():
    def __init__(self, id, name):
        self.id = str(id)
        self.name = name
        self.current_room = None
    
    def setName(self, name):
        self.name = name

    def getName(self, name):
        self.name = name
    
    def set_requested_game_room(self, room):
        self.requestedGameRoom = room

    def set_game_mark(self, gameMark):
        self.gameMark = gameMark

    def start_game_intention(self, gameStart = True):
        self.gameStartIntention = gameStart

    def get_game_intention(self):
       return self.gameStartIntention

class Room():
    def __init__(self, id, name):
        self.id = str(id)
        self.name = name
        self.lead = None
        self.guest = None
        self.ready_player = 0
        self.game = []
        self.watchers = []
        self.status = None

    def isReady(self):
        return self.ready_player == 2

    def isFull(self):
        return self.lead != None and self.guest != None

class Game():
    def __init__(self, id):
        self.id = id
        self.winner = None
        self.room = room
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