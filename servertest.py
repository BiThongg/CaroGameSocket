import numpy as np

from flask_cors import CORS
from flask import Flask, json, request
from flask_socketio import SocketIO, emit

from dto.room import RoomDTO
from room import Room
import room
from user import User
import user

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*")


def serialization(data):
    if isinstance(data, dict):
        return json.dumps(data)
    return data.__dict__


@socketio.on("connect")
def connect():
    print("heelo", request.sid)


@socketio.on("disconnect")
def disconnect():
    print(">> client {} disconnected to server".format(request.sid))


@socketio.on("hehe")
def hehe(payload):
    user1 = User(request.sid, "triet dep trai")
    #
    room = Room("room1", user1)
    # socketio.emit
    #
    # socketio.emit("hehe", {"room": serialization(room), "user": serialization(user1)}, to=request.sid)
    socketio.emit(
        "hehe",
        {
            "room": RoomDTO.to_dto(room),
            "user": User.to_dto(user1),
        },
        to=request.sid,
    )


if __name__ == "__main__":
    socketio.run(app, debug=False)
