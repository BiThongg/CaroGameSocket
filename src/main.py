import numpy as np

from flask_cors import CORS
from datetime import datetime
import uuid, json, random, string
from flask import Flask, session, request, make_response
from flask_socketio import SocketIO, emit, join_room, leave_room, send
import math
from enum import Enum
import jsonpickle

from User import User
from game.Game import Game
from player.AIPlayer import AIPlayer
from player.PersonPlayer import PersonPlayer
from player.Player import Player
from room.Room import Room
from util.point import Point
from util.serializeFilter import serializationFilter
from util.serialize import serialization
from util.nameGeneration import name_generation
from database.data import storage
from auth.authentication import decode_jwt, encode_jwt, authentication_required

app = Flask(__name__)
app.config["SECRET_KEY"] = "CARO_GAME_SUPER_VIP_PRO_MAX"
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.event
def connect():
    print(">> client {} connected to server".format(request.sid))

@socketio.on("access_require")
def accessRequire(payload):
    token = request.headers.get('x-auth-token')
    if token:
        userId = decode_jwt(token)['sub']
        user = storage.users.get(userId)
        if user is None or user.currentToken != token:
            raise Exception(">> Auth Exeption")
        del storage.users[userId]
        user.id = request.sid
        token = encode_jwt(user.id)
        user.currentToken = token
        storage.users[user.id] = user
    else:
        user = User(id=request.sid, name=name_generation(5))
        token = encode_jwt(user.id)
        user.currentToken = token
        storage.users[user.id] = user
        
    socketio.emit("access_success", {
            "token": str(token),
            "user": serialization(user),
        }, to=request.sid
    )

# @socketio.on("register")
# def register(payload):

#     user = User(name=payload["name"])
#     storage.users[userId] = user
#     socketio.emit("register", {
#             "user": serialization(user),
#         },
#         to=userId,
#     )

@authentication_required
@socketio.on("get_users")
def getUser(payload):
    userId = request.sid
    users = list(storage.users.values())
    socketio.emit(
        "list_of_user", {
            "users": serialization(users),
        }, to=userId,
    )

# room event ------------------------------------------------------------------------

@socketio.on("room_list")
def handle_fetch_rooms(payload):
    # get rooms existing
    rooms = list(storage.rooms.values())

    # pagination
    # idxfrom = (payload["page"] - 1) * payload["size"]
    # roomList = rooms[idxfrom : idxfrom + payload["size"] + 1]
    # res = sorted(roomList, key=lambda rm: rm.isFull(), reverse=True)
    # res = res[:payload['size']]
    #
    # # send
    # socketio.emit("list_of_room", {
    #     "page": payload['page'],
    #     "size": payload['size'],
    #     "total_page": math.ceil(len(rooms) / payload['size']),
    #     "rooms": serialization(res)
    #     }, to=request.sid
    # )
    socketio.emit("list_of_room", {"rooms": serialization(rooms)}, to=request.sid)

@socketio.on("create_room")
@authentication_required
def createRoom(payload: dict):
    room = storage.createRoom(payload["room_name"], request.sid)
    socketio.emit("room_created", {
            "room": serialization(room),
        }, to=request.sid,
    )

@authentication_required
@socketio.on("join_room")  # handle for competitor
def joinRoom(payload):
    # find
    user: User = storage.users.get(request.sid)
    room = storage.rooms.get(payload["room_id"])

    # validate
    if room is None or room.isFull():
        socketio.emit(
            "join_room_failed",
            {"message": "Some error happend please try again !"},
            to=request.sid,
        )
    # if avalable
    room.addCompetitor(user)

    # save
    storage.rooms[room.id] = room

    # response
    socketio.emit(
        "joined_room", {"message": "Joined room", "room": serialization(room)},
        to=[room.participantIds()],
    )

@authentication_required
@socketio.on("on_kick")  # handle for competitor
def onKick(payload):
    # find
    room = storage.rooms.get(payload["room_id"])

    # action
    room.kick(payload["guest_id"])

    # save
    storage.rooms[room.id] = room

    # response
    socketio.emit(
        "kicked", {"message": "User was kicked", "room": serialization(room)},
        to=[room.participantIds()],
    )

@authentication_required
@socketio.on("add_bot")
def add_bot(payload):
    # find
    room = storage.rooms.get(payload["room_id"])

    # validate
    if room is None or room.isFull():
        socketio.emit(
            "add_bot_failed",
            {"message": "Some error happend please try again !"},
            to=request.sid,
        )
    # if avalable
    bot = User(name="BOT", id="BOT_{}".format(uuid.uuid4()))
    room.addCompetitor(bot)

    # save
    storage.rooms[room.id] = room

    # response
    socketio.emit(
        "added_bot",
        {"message": "bot added into room", "room": serialization(room)},
        to=[room.owner.info.id],
    )

@authentication_required
@socketio.on("change_status")
def changeStatus(payload):
    room = storage.rooms.get(payload["room_id"])
    userId = request.sid

    # validate
    if room is None:
        socketio.emit(
            "change_status_failed",
            {"message": "Some error happend please try again !"},
            to=request.sid,
        )

    # action
    room.changeStatus(userId)

    # save
    storage.rooms[room.id] = room

    # response
    socketio.emit(
        "status_changed",
        {"room": serialization(room)},
        to=[room.participantIds()],
    )

@authentication_required
@socketio.on("leave_room")  # handle for competitor
def leaveRoom(payload):
    # find
    user = storage.users.get(request.sid)
    room = storage.rooms.get(payload["room_id"])

    # validate
    if room is None:
        socketio.emit(
            "leave_room_failed",
            {"message": "Some error happend please try again !"},
            to=request.sid,
        )

    # if avalable
    room.onLeave(user.id)

    # save
    storage.rooms[room.id] = room

    # response
    socketio.emit(
        "leaved_room",
        {"message": "leaved room", "room": serialization(room)},
        to=[room.participantIds(), request.sid],
    )

@authentication_required
@socketio.on("start_game")
def startGame(payload):
    # find
    user = storage.users.get(request.sid)
    room = storage.rooms.get(payload["room_id"])
    gameType: str = payload["game_type"]

    # validate
    if user.id != room.owner.info.id or room.isReady() == False:
        socketio.emit(
            "start_game_failed",
            {"message": "Some error happend please try again !"},
            to=request.sid,
        )

    # if avalable
    room.gameStart(gameType)

    # save
    storage.rooms[room.id] = room
    for item in list(room.game.players[:]):
        item.game = "__HIDE__"

    # response
    socketio.emit(
        "started_game",
        {
            "message": "Game start !!! Come on",
            "game": serializationFilter(room.game, ["game"]),
        },
        to=[room.participantIds()],
    )

@authentication_required
@socketio.on("move")
def move(payload):
    # find
    print(payload)
    user = storage.users.get(request.sid)
    room = storage.rooms.get(payload["room_id"])
    print(room)
    game = room.game
    pointTmp: dict = payload["point"]
    point = Point(int(pointTmp["x"]), int(pointTmp["y"]))

    player: PersonPlayer = next(
        (player for player in game.players if player.user.id == user.id), None
    )

    # if not player:
    #     socketio.emit(
    #         "move_failed",
    #         {"message": "Some error happend please try again !"},
    #         to=request.sid,
    #     )

    # print(player.game.turn)
    # room.game.handleMove(player, point)
    # player.move(point)

    # save
    storage.rooms[room.id] = room

    # response
    socketio.emit(
        "moved",
        {
            "message": "Moved",
            "game": serializationFilter(room.game, ["game"]),
        },
        to=[room.participantIds()],
    )


@socketio.on("bot_move")
def botMoveSumoku(payload):
    room = storage.getRoom(payload["room_id"])
    if (not room) or (not room.game):
        socketio.emit(
            "bot_move_failed",
            {"message": "Some error happend please try again !"},
            to=request.sid,
        )
    game = room.game
    player: AIPlayer = next(
        (player for player in game.players if player.user.id.startswith("BOT_")), None
    )
    if not player:
        socketio.emit(
            "bot_move_failed",
            {"message": "Some error happend please try again !"},
            to=request.sid,
        )
    else:
        if game.board.__len__() == 3:
            player.makeMoveTictactoe()
        else:
            player.makeMoveSumoku()

    socketio.emit(
        "moved",
        {
            "message": "Bot moved",
            "game": serializationFilter(room.game, ["game"]),
        },
        to=[room.participantIds()],
    )


@socketio.on("bot_move_tictactoe")
def botMoveTictactoe(payload):
    room = storage.getRoom(payload["room_id"])
    if (not room) or (not room.game):
        socketio.emit(
            "bot_move_tictactoe_failed",
            {"message": "Some error happend please try again !"},
            to=request.sid,
        )

    game = room.game
    player: AIPlayer = next(
        (player for player in game.players if player.user.id.startswith("BOT_")), None
    )

    if not player:
        socketio.emit(
            "bot_move_tictactoe_failed",
            {"message": "Some error happend please try again !"},
            to=request.sid,
        )
    else:
        player.makeMoveTictactoe()


# @socketio.on("get_test")
# def handle_get_test(paayload):
#     user1 = User(id=request.sid, name="aaa")
#     user2 = User(id="xnxx2", name="bbb")
#     room = Room("Hello 500 ace")
#     room.lead = request.sid
#     room.guest = user2.id
#     room.ready_player = [request.sid, user2.id]
#     game = Game(user1.id, user2.id)
#     room.game.append(game.id)
#
#     caro_game.rooms[room.id] = room
#     caro_game.users[user1.id] = user1
#     caro_game.users[user2.id] = user2
#     caro_game.games[game.id] = game
#
#     socketio.emit(
#         "get_test",
#         {
#             "code": 200,
#             "message": "Get test",
#             "room": {
#                 "room_info": serialization(room),
#                 "game_time": game.game_time,
#                 "chess_board": game.chess_board,
#             },
#         },
#         to=request.sid,
#     )
#
#
# @socketio.on("room_list")
# def handle_fetch_rooms(payload):
#     # get rooms existing
#     raw = list(caro_game.rooms.values())
#     # pagination
#     idxfrom = (payload["page"] - 1) * payload["size"]
#     dicts = raw[idxfrom : idxfrom + payload["size"] + 1]
#     sorted(dicts, key=lambda x: len(x.ready_player), reverse=True)
#     res = []
#     for room in dicts:
#         res.append(serialization(room))
#     # send
#     socketio.emit(
#             "room_list", {"code": 200, "message": "Room list", "rooms": res , }, to=request.sid
#     )
#
#
# @socketio.on("change_status")
# def handle_change_status(payload):
#     # find
#
#     room = caro_game.rooms.get(payload["room_id"])
#
#     # validate
#     if room.is_in_room(request.sid) == False:
#         socketio.emit(
#             "change_status",
#             {
#                 "code": 400,
#                 "message": "You cannot change status",
#                 "rooms": serialization(room),
#             },
#             to=request.sid,
#         )
#         return
#
#     # set
#     if request.sid in room.ready_player:
#         room.ready_player.remove(request.sid)
#     else:
#         room.ready_player.append(request.sid)
#
#     # save
#     caro_game.rooms[room.id] = room
#
#     # send
#     socketio.emit(
#         "change_status",
#         {
#             "code": 200,
#             "message": "change status successfully",
#             "rooms": serialization(room),
#         },
#         to=[room.guest, room.lead, *room.watchers],
#     )
#
#
# @socketio.on("create_room")
# def handle_create_room(payload):
#     # create
#     room = Room(payload["room_name"])
#
#     # construct relationship
#     user = caro_game.users.get(request.sid)
#     room.lead = user.id
#
#     # save
#     caro_game.rooms[room.id] = room
#     caro_game.users[user.id] = user
#     # response
#     socketio.emit(
#         "create_room",
#         {"code": 200, "message": "Room created", "room": serialization(room)},
#         to=request.sid,
#     )
#
#
# @socketio.on("join_room")
# def handle_join_room(payload):
#     # find
#     room = caro_game.rooms.get(payload["room_id"])
#     # validate
#     if room is None or room.is_full():
#         # if not exist or full
#         # response
#         socketio.emit("join_room", {"code": 404, "message": "Not found room"})
#     else:
#         # if avalable
#         # construct relation ship
#         user = caro_game.users.get(request.sid)
#         room.guest = user.id
#
#         # save
#         caro_game.rooms[room.id] = room
#         caro_game.users[user.id] = user
#         # response
#         socketio.emit(
#             "join_room",
#             {"code": 200, "message": "Joined room", "room": serialization(room)},
#             to=[room.guest, room.lead, *room.watchers],
#         )
#
#
# @socketio.on("room_start")
# def handle_start_game(payload):
#     room = caro_game.rooms.get(payload["room_id"])
#     if room is None or room.is_ready() == False:
#         socketio.emit(
#             "room_start",
#             {
#                 "code": 400,
#                 "message": "Can't start because not enough members are ready",
#             },
#             to=[request.sid],
#         )
#     else:
#         # create
#         game = Game(room.lead, room.guest)
#
#         # relationship
#         game.room = room.id
#         room.game.append(game.id)
#
#         # save
#         caro_game.games[game.id] = game
#         caro_game.rooms[room.id] = room
#
#         # response
#         socketio.emit(
#             "room_start",
#             {
#                 "code": 200,
#                 "message": "Starting game play success",
#                 "data": {
#                     "room": serialization(room),
#                     "game_time": game.game_time,
#                     "chess_board": serialization(game.chess_board.tolist()),
#                 },
#             },
#             to=[*room.ready_player, *room.watchers],
#         )
#
#
# @socketio.on("leave_room")
# def handle_leave_room(payload):
#     # find
#     room = caro_game.rooms.get(payload["room_id"])
#
#     # validate
#     if room is None or room.is_in_room(request.sid) == False:
#         # if not exist or not in room
#         # response
#         socketio.emit("leave_room", {"code": 400, "message": "Cannot leave room"})
#     else:
#         # if avalable
#         user = caro_game.users.get(request.sid)
#         room.leave_room(request.sid)  # change automatically lead room
#
#         # save
#         caro_game.rooms[room.id] = room
#         caro_game.users[user.id] = user
#
#         # response
#         socketio.emit(
#             "leave_room",
#             {"code": 200, "message": "leaved room", "room": serialization(room)},
#             to=[request.sid, room.lead, *room.watchers],
#         )
#
#
# @socketio.on("hehe")
# def handle_test(payload):
#     print(payload)
#     socketio.emit("test", {"code": 199, "message": "Test success"}, to=request.sid)
#
#
# # game event -----------------------------------------------------------------------------------------------------
#
# # @socketio.on('strike_out')
# # def handle_strike_out(payload):
# #     game = caro_game.games.get(payload['game_id'])
# #     # validate
# #     if(game.is_can_strike(request.ids) ==  False):
# #         socketio.emit('strike_out', {
# #             "code": 400,
# #             "message": 'Cannot strike out'
# #         }, to=request.ids)
#
# #     mark = payload['mark']
# #     if game.is_end_game(mark):
# #         game.winner = request.sid
# #         socketio.emit('strike_out', {
# #             "code": 200,
# #             "message": 'End game',
# #             "game": serialization(game)
# #         }, to=request.ids)
# #     else:
#
#
if __name__ == "__main__":
    try:
        socketio.run(app, debug=False)
    except Exception as e:
        print(f"Caught a global exception: {e}")
