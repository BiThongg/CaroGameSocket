from flask_cors import CORS
from flask import Flask, request
from flask_socketio import SocketIO, emit

from User import User
from player.AIPlayer import AIPlayer
from room.Room import Room
from util.point import Point
from util.serializeFilter import serializationFilter
from util.serialize import serialization
from database.data import storage
from auth.authentication import authentication_required

app = Flask(__name__)
app.config["SECRET_KEY"] = "CARO_GAME_SUPER_VIP_PRO_MAX"
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*")


@socketio.event
def connect():
    user_id = request.args.get("user_id")
    if user_id in storage.users:
        user = storage.users[user_id]
        user.sid = request.sid
    else:
        emit("error", {"message": "User not found"}, to=request.sid)


@socketio.on("register")
def register(payload):
    user = User(name=payload["name"], sid=request.sid)
    user_id = user.id
    storage.users[user_id] = user

    socketio.emit(
        "register",
        {
            "user": serialization(user),
        },
        to=user.sid,
    )


# @socketio.on("access_require")
# def accessRequire(payload):
#     token = request.headers.get('x-auth-token')
#     if token:
#         userId = decode_jwt(token)['sub']
#         user = storage.users.get(userId)
#         if user is None or user.currentToken != token:
#             raise Exception(">> Auth Exeption")
#         del storage.users[userId]
#         user.id = request.sid
#         token = encode_jwt(user.id)
#         user.currentToken = token
#         storage.users[user.id] = user
#     else:
#         user = User(id=request.sid, name=name_generation(5))
#         token = encode_jwt(user.id)
#         user.currentToken = token
#         storage.users[user.id] = user
#
#     socketio.emit("access_success", {
#             "token": str(token),
#             "user": serialization(user),
#         }, to=socketio.id
#     )


@authentication_required
@socketio.on("get_users")
def getUser(payload):
    userId = request.sid
    users = list(storage.users.values())
    socketio.emit(
        "list_of_user",
        {
            "users": serialization(users),
        },
        to=userId,
    )


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
def getRoomFromUserId(payload):
    user_id = payload["user_id"]
    room = storage.getRoomByUserId(user_id)

    if room:
        socketio.emit(
            "room_info",
            {
                "room": serialization(room),
            },
            to=request.sid,
        )
    else:
        emit("error", {"message": "Room not found"}, to=request.sid)


@socketio.on("join_room")
def joinRoom(payload):
    user: User = storage.users.get(payload["user_id"])
    room: Room = storage.rooms.get(payload["room_id"])

    if not room:
        socketio.emit(
            "join_room_failed",
            {"message": "Some error happend please try again !"},
            to=request.sid,
        )
    # join_room(room.id)

    room.onJoin(user)
    socketio.emit(
        "joined_room",
        {"message": "Joined room", "room": serialization(room)},
        to=room.participantIds(),
    )


@socketio.on("kick")
def onKick(payload):
    room: Room = storage.rooms.get(payload["room_id"])

    room.kick(payload["owner_id"], payload["kick_id"])
    socketio.emit(
        "kicked",
        {"message": "User was kicked", "room": serialization(room)},
        to=room.participantIds(),
    )


@socketio.on("add_bot")
def add_bot(payload):
    room: Room = storage.rooms.get(payload["room_id"])

    if room is None or room.isFull():
        socketio.emit(
            "add_bot_failed",
            {"message": "Some error happend please try again !"},
            to=request.sid,
        )

    room.addBot()

    socketio.emit(
        "added_bot",
        {"message": "bot added into room", "room": serialization(room)},
        to=room.participantIds(),
    )


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

    room.changeStatus(userId)

    socketio.emit(
        "status_changed",
        {"room": serialization(room)},
        to=room.participantIds(),
    )


@socketio.on("change_game_type")
def changeGameType(payload):
    room = storage.rooms.get(payload["room_id"])
    gameType: str = payload["game_type"]

    socketio.emit(
        "game_type_changed",
        {"game_type": gameType, "room_id": room.id},
        to=room.participantIds(),
    )


@socketio.on("leave_room")  # handle for competitor
def leaveRoom(payload):
    user = storage.users.get(request.sid)
    room = storage.rooms.get(payload["room_id"])

    if room is None:
        socketio.emit(
            "leave_room_failed",
            {"message": "Some error happend please try again !"},
            to=request.sid,
        )

    room.onLeave(user.id)

    # save
    storage.rooms[room.id] = room

    # response
    socketio.emit(
        "leaved_room",
        {"message": "leaved room", "room": serialization(room)},
        to=room.participantIds(),
    )


@socketio.on("start_game")
def startGame(payload):
    user: User = storage.users.get(payload["user_id"])
    room: Room = storage.rooms.get(payload["room_id"])
    gameType: str = payload["game_type"]

    if not room.checkConditionForStart(user_id=user.id):
        socketio.emit(
            "start_game_failed",
            {"message": "Some error happend please try again !"},
            to=request.sid,
        )

    print(vars(room))

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
def move(payload):
    user: User = storage.users.get(payload["user_id"])
    room: Room = storage.rooms.get(payload["room_id"])
    game = room.game

    if not game.checkPlayer(user.id):
        socketio.emit(
            "move_failed",
            {"message": "Some error happend please try again !"},
            to=request.sid,
        )

    player = game.getPlayer(user_id=user.id)
    pointTmp: dict = payload["point"]
    point = Point(int(pointTmp["x"]), int(pointTmp["y"]))

    player.move(point)

    socketio.emit(
        "moved",
        {
            "message": "Moved",
            "game": serializationFilter(room.game, ["game"]),
        },
        to=room.participantIds(),
    )


@socketio.on("bot_move")
def botMoveSumoku(payload):
    room = storage.getRoom(payload["room_id"])
    if (not room) or (not room.game):
        socketio.emit(
            "bot_move_failed",
            {"message": "Some error happend please try again !"},
            to=room.participantIds(),
        )

    game = room.game
    player: AIPlayer = game.getBot()

    if not player:
        socketio.emit(
            "bot_move_failed",
            {"message": "Some error happend please try again !"},
            to=[room.participantIds()],
        )

    if game.board.__len__() == 3:
        player.makeMoveTictactoe()
    else:
        player.makeMoveSumoku()

    socketio.emit(
        "moved",
        {
            "message": "Bot moved",
            "game": serializationFilter(game, ["game"]),
        },
        to=room.participantIds(),
    )


if __name__ == "__main__":
    try:
        socketio.run(app, debug=False)
    except Exception as e:
        print(f"Caught a global exception: {e}")
