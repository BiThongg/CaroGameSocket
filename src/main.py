from flask import request
from flask_socketio import emit

from User import User
from player.AIPlayer import *
from player.PersonPlayer import *
from player.Player import *
from room.Room import Room
from util.point import Point
from util.serializeFilter import serializationFilter
from util.serialize import serialization
from database.data import storage
from auth.authentication import user_infomation_filter
from config import *


@socketio.event
@user_infomation_filter
def connect(user: User, payload: dict):
    if user is not None:
        user.sid = request.sid
    else:
        emit("error", {"message": "User not found"}, to=request.sid)


# def beforeReconnect(id: str):
#     rooms: list[Room] = storage.getRooms()
#     for room in rooms:
#         if id in room.participantIds():
#             pass


@socketio.on("register")
def register(payload):
    user = User(name=payload["name"], sid=request.sid)
    user_id = user.id
    storage.users[user_id] = user
    socketio.emit("register", {"user": serialization(user)}, to=user.sid)


@socketio.on("get_users")
@user_infomation_filter
def getUser(user: User, payload: dict):
    users = list(storage.users.values())
    socketio.emit(
        "list_of_user",
        {"users": serialization(users)},
        to=user.sid,
    )


@socketio.on("room_list")
def handle_fetch_rooms(payload):
    # get rooms existing
    # rooms = list(storage.rooms.values())
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
    # socketio.emit("list_of_room", {"rooms": serialization(rooms)}, to=request.sid)
    pass


@socketio.on("create_room")
def createRoom(payload):
    room = storage.createRoom(payload["room_name"], payload["user_id"])

    socketio.emit(
        "room_created",
        {
            "room": serialization(room),
        },
        to=room.participantIds(),
    )


@socketio.on("get_room")
@user_infomation_filter
def getRoomFromUserId(user: User, payload: dict):
    room = next(
        (
            room
            for room in storage.rooms.values()
            if room.owner.info.id == user.id or room.competitor.info.id == user.id
        ),
        None,
    )

    if room:
        socketio.emit(
            "room_info",
            {
                "room": serialization(room),
            },
            to=request.sid,
        )
        return
    socketio.emit("error", {"message": "Room not found"}, to=request.sid)


@socketio.on("join_room")
@user_infomation_filter
def joinRoom(user: User, payload: dict):
    room: Room = storage.rooms.get(payload["room_id"])

    if not room:
        socketio.emit(
            "join_room_failed",
            {"message": "Some error happened please try again !"},
            to=request.sid,
        )

    room.onJoin(user)

    socketio.emit(
        "joined_room",
        {"message": "Joined room", "room": serialization(room)},
        to=room.participantIds(),
    )


@socketio.on("kick")
@user_infomation_filter
def onKick(user: User, payload: dict):
    room: Room = storage.rooms.get(payload["room_id"])

    receivers = room.participantIds()
    room.kick(user.id, payload["kick_id"])

    socketio.emit(
        "kicked",
        {"message": "User was kicked", "room": serialization(room)},
        to=receivers,
    )


@socketio.on("add_bot")
@user_infomation_filter
def add_bot(user: User, payload: dict):
    room: Room = storage.rooms.get(payload["room_id"])

    if room is None or room.isFull() or user.id != room.getOwnerInfo().id:
        socketio.emit(
            "add_bot_failed",
            {"message": "Some error happend please try again !"},
            to=room.participantIds(),
        )

    room.addBot()

    socketio.emit("added_bot", {"room": serialization(room)}, to=room.participantIds())


@socketio.on("change_status")
@user_infomation_filter
def changeStatus(user: User, payload: dict):
    # find
    room = storage.rooms.get(payload["room_id"])
    # validate
    if room is None:
        socketio.emit(
            "change_status_failed",
            {"message": "Some error happend please try again !"},
            to=request.sid,
        )
    # implement
    room.changeStatus(user.id)
    # response
    socketio.emit(
        "status_changed", {"room": serialization(room)}, to=room.participantIds()
    )


@socketio.on("change_game_type")
@user_infomation_filter
def changeGameType(user: User, payload: dict):
    room: Room = storage.rooms.get(payload["room_id"])
    gameType: str = payload["game_type"]

    if user.id == room.owner.info.id:
        socketio.emit(
            "game_type_changed",
            {"game_type": gameType, "room_id": room.id},
            to=room.participantIds(),
        )


@socketio.on("leave_room")
@user_infomation_filter
def leaveRoom(user: User, payload: dict):
    room: Room = storage.rooms.get(payload["room_id"])
    if room is None:
        socketio.emit(
            "leave_room_failed",
            {"message": "Some error happend please try again !"},
            to=request.sid,
        )
    room.onLeave(user.id)

    socketio.emit(
        "leaved_room",
        {"message": "leaved room", "room": serialization(room)},
        to=room.participantIds() + [user.sid],
    )


@socketio.on("start_game")
@user_infomation_filter
def startGame(user: User, payload: dict):
    room: Room = storage.rooms.get(payload["room_id"])
    gameType: str = payload["game_type"]

    if not room.checkConditionForStart(user_id=user.id):
        socketio.emit(
            "start_game_failed",
            {"message": "Some error happend please try again !"},
            to=request.sid,
        )

    room.gameStart(gameType)
    socketio.emit(
        "started_game",
        {
            "message": "Game start !!! Come on",
            "game": serializationFilter(room.game, ["game"]),
        },
        to=room.participantIds(),
    )


@socketio.on("move")
@user_infomation_filter
def move(user: User, payload: dict):
    room: Room = storage.rooms.get(payload["room_id"])

    # valid
    if room is None or room.game is None:
        socketio.emit(
            "move_failed", {"message": "Not found room or game !"}, to=request.sid
        )

    game: Game = room.game
    if not game.checkPlayer(user.id):
        socketio.emit(
            "move_failed",
            {"message": "You are not permission to move !"},
            to=request.sid,
        )

    point: Point = Point(x=payload["point"]["x"], y=payload["point"]["y"])
    game.getPlayer(user.id).move(point)

    gameEndInfo: dict = game.getGameEndInfo()

    game.updateTurn()
    socketio.emit(
        "moved",
        {"message": "Moved", "game": serializationFilter(room.game, ["game"])},
        to=room.participantIds(),
    )

    if gameEndInfo is not None:
        game.endGame()
        room.game = None
        socketio.emit(
            "ended_game",
            {
                "message": f"{user.name} ({serialization(gameEndInfo['symbol'])}) wins !",
                "winner": serialization(gameEndInfo),
            },
            to=room.participantIds(),
        )
        return

    if game.isFullBoard():
        game.endGame()
        room.game = None
        socketio.emit(
            "ended_game", {"message": "Draw game !"}, to=room.participantIds()
        )


@socketio.on("bot_move")
def botMoveSumoku(payload: dict):
    room: Room = storage.getRoom(payload["room_id"])

    if (not room) or (not room.game):
        socketio.emit(
            "bot_move_failed",
            {"message": "Some error happened please try again !"},
            to=room.participantIds(),
        )

    game: Game = room.game
    player: AIPlayer = game.getBot()

    if not player:
        socketio.emit(
            "bot_move_failed",
            {"message": "Some error happend please try again !"},
            to=room.participantIds(),
        )
        return

    player.makeMove()

    gameEndInfo: dict = game.getGameEndInfo()

    game.updateTurn()
    socketio.emit(
        "moved",
        {"message": "Bot moved", "game": serializationFilter(game, ["game"])},
        to=room.participantIds(),
    )

    if gameEndInfo is not None:
        game.endGame()
        room.game = None
        socketio.emit(
            "ended_game",
            {
                "message": f"BOT ({serialization(gameEndInfo['symbol'])}) wins !",
                "winner": serialization(gameEndInfo),
            },
            to=room.participantIds(),
        )
        return

    if game.isFullBoard():
        game.endGame()
        room.game = None
        socketio.emit(
            "ended_game", {"message": "Draw game !"}, to=room.participantIds()
        )


# def endGame(winner: Player, roomId: str):
#     room: Room = storage.getRoom(roomId)

#     if (not room) or (not room.game):
#         socketio.emit("error",
#             {"message": "Some error happend please try again !"},
#             to=room.participantIds()
#         )

#     room.game = None

#     socketio.emit("ended_game", {
#         "message": "End Game",
#         "winner": f"{winner.user.name} ({serialization(winner.symbol)}) wins !"
#     }, to=room.participantIds())
if __name__ == "__main__":
    try:
        socketio.run(app, debug=False)
    except Exception as e:
        print(f"Caught a global exception: {e}")
