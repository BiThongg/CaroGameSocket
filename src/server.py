import jsonpickle
import numpy as np

from flask_cors import CORS
from datetime import datetime
import uuid, json, random, string
from flask import Flask, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room, send

from src.util.storage import Storage
from src.room.user import User

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
CORS(app, resources={r"/*": {"origins": "*"}})

socketio = SocketIO(app, cors_allowed_origins="*")


def name_generation(length):
    characters = string.ascii_letters
    random_string = "".join(random.choices(characters, k=length))
    return random_string


def serialization(data):
    if isinstance(data, dict):
        return json.dumps(data)
    return data.__dict__


storage = Storage()


# caro_game = Caro()

#                   Caro
#                    |
#                   Room
#                  /    \
#               Game    User

# user event ------------------------------------------------------------------------


@socketio.event("connect")
def connect():
    requestId = request.sid
    user = User(id=requestId, name=name_generation(5))

    storage.users[requestId] = user
    socketio.emit(
        "connect",
        {
            "code": 200,
            "message": "Connected to server",
            "user": jsonpickle.encode(user),
        },
        to=requestId,
    )
    print(">> client {} connected to server".format(requestId))


@socketio.event("disconnect")
def disconnect():
    requestId = request.sid
    storage.users.pop(requestId)
    print(">> client {} disconnected from server".format(requestId))


# @socketio.on("player_information")
# def handle_player_information(payload):
#     user = users.get(request.sid)
#     socketio.emit(
#         "player_information",
#         {
#             "code": 200,
#             "message": "Player information",
#             "player": jsonpickle.encode(user),
#         },
#         to=user.id,
#     )


@socketio.on("get_user")
def get_user(payload):
    requestId = request.sid
    user = storage.users.get(requestId)
    socketio.emit(
        "get_user",
        {
            "code": 200,
            "message": "Get user",
            "user": serialization(user),
        },
        to=requestId,
    )


@socketio.on("get_users")
def get_users(payload):
    requestId = request.sid
    users = list(storage.users.values())
    socketio.emit(
        "get_users",
        {
            "code": 200,
            "message": "Get users",
            "users": list(map(lambda x: serialization(x), users)),
        },
        to=requestId,
    )


@socketio.on("register")
def register(payload):
    requestId = request.sid
    user = User(id=requestId, name=payload["name"])
    storage.users[requestId] = user
    socketio.emit(
        "register",
        {
            "code": 200,
            "message": "Register success",
            "user": serialization(user),
        },
        to=requestId,
    )


# room event ------------------------------------------------------------------------


# @socketio.on("get_test")
# def handle_get_test(payload):
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
    socketio.run(app, debug=False)