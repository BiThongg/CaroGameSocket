import numpy as np
from user import User
from room import Room
from game import Game
from caro import Caro
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
    if isinstance(data, dict) or isinstance(data, list):
        return json.dumps(data)
    return data.__dict__ 

caro_game = Caro()

#                   Caro
#                    |
#                   Room
#                  /    \   
#               Game    User


@socketio.on('hehe')
def handle_hehe():
    socketio.emit('test', {
        "minh_triet": 'chicken'
    }, to=request.sid)

# user event ------------------------------------------------------------------------

@socketio.event
def connect():
    user = User(id = request.sid, name = name_generation(5))
    caro_game.users[user.id] = user
    print(">> client {} connected to server".format(user.id))

@socketio.event
def disconnect():
    del caro_game.users[request.sid]
    print(">> client {} disconnected to server".format(request.sid))

@socketio.on('player_information')
def handle_player_information(payload):
    user = caro_game.users.get(request.sid)
    user.name = payload['name']
    caro_game.users[request.sid] = user
    socketio.emit('player_information', {
        "code": 200,
        "message": 'Player information',
        "player": serialization(user)
    }, to = user.id)

# room event ------------------------------------------------------------------------

@socketio.on('get_test')
def handle_get_test(payload):
    # chess_board = json.loads(payload['chess_board'])
    # print(chess_board[0][1] + 2)
    user1 = User(id=request.sid, name="aaa")
    user2 = User(id="xnxx2", name="bbb")
    room = Room("Hello 500 ace")
    room.lead = request.sid
    room.guest = user2.id
    room.ready_player = [request.sid, user2.id]
    game = Game(user1.id, user2.id)
    room.game.append(game.id)

    caro_game.rooms[room.id] = room
    caro_game.users[user1.id] = user1
    caro_game.users[user2.id] = user2
    caro_game.games[game.id] = game

    socketio.emit('get_test', {
        "code": 200,
        "message": 'Get test',
        "room": {
            'room_info': serialization(room),
            'game_time': game.game_detail,
            'chess_board': json.dumps(game.chess_board.tolist())
        },
        "game": serialization(game)
    }, to=request.sid)


@socketio.on('room_list')
def handle_fetch_rooms(payload):
    # get rooms existing
    raw = list(caro_game.rooms.values())
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
    
    room = caro_game.rooms.get(payload['room_id'])

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
    caro_game.rooms[room.id] = room

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
    user = caro_game.users.get(request.sid)
    room.lead = user.id

    # save
    caro_game.rooms[room.id] = room
    caro_game.users[user.id] = user
    # response
    socketio.emit('create_room', {
        "code": 200,
        "message": 'Room created',
        "room": serialization(room)
    }, to = request.sid)

@socketio.on('join_room')
def handle_join_room(payload):
    # find
    room = caro_game.rooms.get(payload['room_id'])
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
        user = caro_game.users.get(request.sid)
        room.guest = user.id

        # save
        caro_game.rooms[room.id] = room
        caro_game.users[user.id] = user

        # response
        # socketio.emit('join_room', {
        #     "code": 200,
        #     "message": 'Joined room',
        #     "room": serialization(room)
        # }, to = [room.guest, room.lead, *room.watchers])
        handle_start_game(payload)

@socketio.on('room_start')
def handle_start_game(payload):
    room = caro_game.rooms.get(payload['room_id'])
    # if room is None or room.is_ready() == False:
    #     socketio.emit('room_start', {
    #         "code": 400,
    #         "message": "Can't start because not enough members are ready",
    #     }, to = [request.sid])
    # else:
        # create
    game = Game(room.lead, room.guest)

    # relationship
    game.room_id = room.id
    room.game_ids.append(game.id)

    # save
    caro_game.games[game.id] = game
    caro_game.rooms[room.id] = room

    # response
    socketio.emit('room_start', {
        "code": 200,
        "message": 'Starting game play success',
        "data": {
            "room": serialization(room),
            "game_id": game.id,
            "game_time": game.game_detail,
            "chess_board": serialization(game.chess_board.tolist())
        } 
    }, to = [room.lead, room.guest, *room.watchers])

@socketio.on('leave_room')
def handle_leave_room(payload):
    # find
    room = caro_game.rooms.get(payload['room_id'])

    # validate
    if room is None or room.is_in_room(request.sid) == False:
        # if not exist or not in room
        # response
        socketio.emit('leave_room', {
            "code": 400,
            "message": 'Cannot leave room'
        })
        return
    # if avalable
    user = caro_game.users.get(request.sid)
    room.leave_room(request.sid) # change automatically lead room 

    # save
    caro_game.rooms[room.id] = room
    caro_game.users[user.id] = user

    # response
    socketio.emit('leave_room', {
        "code": 200,
        "message": 'leaved room',
        "room": serialization(room)
    }, to = [room.guest, room.lead, *room.watchers])

# game event -----------------------------------------------------------------------------------------------------

@socketio.on('strike_out')
def handle_strike_out(payload):
    # find
    game = caro_game.games.get(payload['game_id'])
    room = caro_game.rooms.get(game.room_id)

    # validate is player of this room and is my turn ?
    if game.is_can_strike(request.sid) == False and game.is_my_turn(request.sid) == False:
        socketio.emit('strike_out', {
            "code": 400,
            "message": 'Cannot strike out'
        }, to=request.sid)
        return

    # validate out of time can strike out
    if game.validiate_time_limit_set_latest_time_and(request.sid) == False:
        game.winner = game.game_detail[request.sid]['competitor_id']
        socketio.emit('end_game', {
            "code": 200,
            "message": 'End end',
            "room": serialization(room),
            "game_id": game.id,
            "game_time": game.game_detail,
            "chess_board": serialization(game.chess_board.tolist())
        }, to=[room.guest, room.lead, room.watchers])
        return

    # mark point
    position = payload['position']
    game.mark(request.sid, position)

    if game.is_end_game():
        # end game
        game.winner = request.sid
        socketio.emit('end_game', {
            "code": 200,
            "message": 'End game',
            "game": serialization(game)
        }, to=request.sid)
    else:
        # continue next turn
        socketio.emit('strike_out', {
            "code": 200,
            "message": 'Next turn',
            "room": serialization(room),
            "game_id": game.id,
            "game_time": game.game_detail,
            "chess_board": serialization(game.chess_board.tolist())
        }, to=[room.guest, room.lead, *room.watchers])


if __name__ == "__main__":
    socketio.run(app, debug=True)