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
    if isinstance(data, dict):
        return json.dumps(data)
    return data.__dict__ 

rooms = {}
users = {}
games = {}

# user event ------------------------------------------------------------------------

@socketio.event
def connect():
    global users
    user = User(id = request.sid, name = name_generation(5))
    users[user.id] = user
    print(">> client {} connected to server".format(user.id))

@socketio.event
def disconnect():
    global users
    del users[request.sid]
    print(">> client {} disconnected to server".format(request.sid))

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

# room event ------------------------------------------------------------------------

@socketio.on('room_list')
def handle_fetch_rooms(payload):
    # get rooms existing
    raw = list(rooms.values())
    # pagination
    idxfrom = (payload['page'] - 1) * payload['size']
    dicts = raw[idxfrom : idxfrom + payload['size'] + 1]
    sorted(dicts, key=lambda x: len(x.ready_player), reverse=True)
    res = []
    for room in dicts:
        res.append(serialization(room))
    # send
    socketio.emit('room_list', {
        "code": 200,
        "message": 'Room list',
        "rooms": res
    }, to = request.sid)

@socketio.on('change_status')
def handle_change_status(payload):
    # find
    global rooms
    room = rooms.get(payload['room_id'])
    # validate
    if room.is_in_room(request.sid) == False:
        socketio.emit('change_status', {
            "code": 400,
            "message": 'You cannot change status',
            "rooms": serialization(room)
        }, to = request.sid)
        return
    # set
    if request.sid in room.ready_player:
        room.ready_player.remove(request.sid)
    else:
        room.ready_player.append(request.sid)
    # save
    rooms[room.id] = room
    # send
    socketio.emit('change_status', {
        "code": 200,
        "message": 'change status successfully',
        "rooms": serialization(room)
    }, to = [room.guest, room.lead, *room.watchers])

@socketio.on('create_room')
def handle_create_room(payload):
    # create
    room = Room(payload['room_name'])
    # construct relationship
    user = users.get(request.sid)
    room.lead = user.id
    user.current_room = room.id
    # save
    global rooms
    rooms[room.id] = room
    users[user.id] = user
    # response
    socketio.emit('create_room', {
        "code": 200,
        "message": 'Room created',
        "room": serialization(room)
    }, to = request.sid)

@socketio.on('join_room')
def handle_join_room(payload):
    # find
    global rooms
    room = rooms.get(payload['room_id'])
    # validate
    if room is None or room.is_full():
        # if not exist or full
        # response
        socketio.emit('join_room', {
            "code": 404,
            "message": 'Not found room'
        })
    else:
        # if avalable
        # construct relation ship
        user = users.get(request.sid)
        room.guest = user.id

        # save
        rooms[room.id] = room
        users[user.id] = user
        # response
        socketio.emit('join_room', {
            "code": 200,
            "message": 'Joined room',
            "room": serialization(room)
        }, to = [room.guest, room.lead, *room.watchers])

@socketio.on('room_start')
def handle_start_game(payload):
    global rooms
    room = rooms.get(payload['room_id'])
    if room is None or room.is_ready() == False:
        socketio.emit('room_start', {
            "code": 400,
            "message": "Can't start because not enough members are ready",
        }, to = [request.sid])
    else:
        # create
        global games
        game = Game()
        # relationship
        game.room = room.id
        room.game.append(game.id)
        # save
        games[game.id] = game
        rooms[room.id] = room
        # response
        socketio.emit('room_start', {
            "code": 200,
            "message": 'Starting game play success',
            "room": serialization(room)
        }, to = [*room.ready_player, *room.watchers])

@socketio.on('leave_room')
def handle_leave_room(payload):
    # find
    global rooms
    room = rooms.get(payload['room_id'])
    # validate
    if room is None or room.is_in_room(request.sid) == False:
        # if not exist or not in room
        # response
        socketio.emit('leave_room', {
            "code": 400,
            "message": 'Cannot leave room'
        })
    else:
        # if avalable
        user = users.get(request.sid)
        room.leave_room(request.sid) # change automatically lead room 

        # save
        rooms[room.id] = room
        users[user.id] = user

        # response
        socketio.emit('leave_room', {
            "code": 200,
            "message": 'leaved room',
            "room": serialization(room)
        }, to = [request.sid, room.lead, *room.watchers])

# game event -----------------------------------------------------------------------------------------------------

@socketio.on('strike_out')
def handle_strike_out(payload):
    # create
    room = Room(payload['room_name'])
    # construct relationship
    user = users.get(request.sid)
    room.lead = user.id
    user.current_room = room.id
    # save
    global rooms
    rooms[room.id] = room
    users[user.id] = user
    # response
    socketio.emit('create_room', {
        "code": 200,
        "message": 'Room created',
        "room": serialization(room)
    }, to = request.sid)





if __name__ == "__main__":
    socketio.run(app, debug=True)