import socketio


# Standard Python
sio = socketio.Client()

@sio.event
def connect():
    print("Connected to the server")
    sio.emit('join', {'room': 'room1'})


@sio.event
def message(data):
    print("message received: ", data)


@sio.event
def disconnect():
    print("disconnected from server")




sio.connect("http://localhost:5000")
sio.emit("message", {"username": "tempmonkey", "room": "room1", "message": "Hello EveryBody!"})
sio.emit("send_message_to_room", {"room": "room1", "message": "Hello Room1!"})
sio.emit("leave", {"room": "room1", "msg": "I'm leaving the room"})
sio.wait()
