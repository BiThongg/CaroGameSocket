import numpy as np
from entities import *
from flask_cors import CORS
from datetime import datetime
import uuid, json, random, string
from flask import Flask, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
CORS(app, resources = {r"/*":{
    "origins": "*"
}})

socketio = SocketIO(app,cors_allowed_origins="*")

def name_generation(length):
    characters = string.ascii_letters
    random_string = ''.join(random.choices(characters, k=length))
    return random_string

def serialization(data):
    return json.dumps(data.__dict__)

rooms = {}
users = {}
games = {}
records = {}
# request.ids = uuid
uuid_mapping = {}

# user event

@socketio.event
def connect():
    user = User(id = request.sid, name = name_generation(5))
    global users
    users[user.id] = user
    print(">> client {} connected to server".format(user.id))

@socketio.event
def disconnect():
    global users
    user = users.get(request.sid)
    del users[request.sid]
    print(">> client {} disconnected to server".format(user.id))

@socketio.on('player_information')
def handle_player_information(payload):
    user = users.get(request.sid)
    user.name = payload['name']
    users[request.sid] = user
    socketio.emit('player_information', {
        "code": 200,
        "message": 'Player information',
        "player": serialization(user)
    }, to = user.id)

# room event

@socketio.on('room_list')
def handle_fetch_rooms(payload):
    res = []
    for room in rooms.values():
        res.append(serialization(room))

    socketio.emit('room_list', {
        "code": 200,
        "message": 'Room list',
        "rooms": res
    }, to = request.sid)

@socketio.on('ready')
def handle_ready(payload):
    global rooms
    room = rooms.get(payload['room_id'])

    room.ready_player = room.ready_player + 1
    rooms[room.id] = room

    socketio.emit('room_list', {
        "code": 200,
        "message": 'Room list',
        "rooms": room
    }, to = [room.guest, room.lead])

@socketio.on('wait')
def handle_ready(payload):
    global rooms
    room = rooms.get(payload['room_id'])

    if room.ready_player < 1:
        
    room.ready_player = room.ready_player - 1
    rooms[room.id] = room

    socketio.emit('room_list', {
        "code": 200,
        "message": 'Room list',
        "rooms": room
    }, to = [room.guest, room.lead])

@socketio.on('ready')
def handle_ready(payload):
    global rooms
    room = rooms.get(payload['room_id'])

    room.ready_player = room.ready_player + 1
    rooms[room.id] = room

    socketio.emit('room_list', {
        "code": 200,
        "message": 'Room list',
        "rooms": room
    }, to = [room.guest, room.lead])

@socketio.on('create_room')
def handle_create_room(payload):
    # create
    room = Room(uuid.uuid4(), payload['room_name'])

    # construct relationship
    user = users.get(request.sid)
    room.lead = users.get(request.sid)
    user.current_room = room

    # save
    global rooms
    rooms[room.id] = room

    # response
    socketio.emit('create_room', {
        "code": 200,
        "message": 'Room created',
        "room": serialization(room)
    }, to = request.sid)

@socketio.on('join_room')
def handle_join_room(payload):
    global rooms

    # find
    room = rooms.get(payload['room_id'])

    if room is None:
        # if not exist
        # response
        socketio.emit('join_room', {
            "code": 404,
            "message": 'Not found room'
        })
    else:
        # if exist
        # construct relation ship
        user = users.get(request.sid)
        room.guest = user
        user.current_room = room

        # save
        rooms[room.id] = room

        # response
        socketio.emit('join_room', {
            "code": 200,
            "message": 'Joined room',
            "room": serialization(room)
        }, to = [room.id, request.sid])

@socketio.on('room_start')
def handle_room_start(payload):
    room = rooms.get(payload['room_id'])
    if room is None or room.isAvailable() == False:
        socketio.emit('room_start', {
            "code": 404,
            "message": 'Room not available or not found'
        })
    else:
        game = 

# @socketio.on("message")
# def handle_message(data):
#     print("Message received: " + str(data))
#     socketio.emit("message", {"data": "Message received"})
#     send("Message received hahah")


# @socketio.on("join")
# def handle_join(data):
#     room = data["room"]
#     join_room(room)
#     send("Joined room: " + room, room=room)
#     print("Joined room: " + room)

# @socketio.on("leave")
# def handle_leave(data):
#     room = data["room"]
#     msg = data["msg"]
#     leave_room(room)
#     send("Left room: " + room, room=room)
#     send(msg)
#     print("Left room: " + room)

# @socketio.on("join", namespace= "/chat")
# def handle_join_chat(data):
#     room = data["room"]
#     join_room(room)
#     send("Joined room: " + room, room=room)
#     emit("message", {"data": "Joined room: " + room})
#     print("Joined room: " + room)

# @socketio.on("send_message_to_room")
# def handle_send_message_to_room(data):
#     room = data["room"]
#     message = data["message"]
#     send(message, room=room)
#     print("Message sent to room: " + room)

    if __name__ == "__main__":
    # make hot reloading 
        socketio.run(app, debug=True)