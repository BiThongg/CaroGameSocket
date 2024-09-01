from flask import Flask
from flask_socketio import SocketIO, emit, join_room, leave_room, send

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app)


@socketio.on("connect")
def handle_connect():
    print("Client connected")
    socketio.emit("message", {"data": "Connected"})


@socketio.on("disconnect")
def handle_disconnect():
    print("Client disconnected")
    send("Client disconnected hahah")
    socketio.emit("message", {"data": "Disconnected"})


@socketio.on("message")
def handle_message(data):
    print("Message received: " + str(data))
    socketio.emit("message", {"data": "Message received"})
    send("Message received hahah")


@socketio.on("join")
def handle_join(data):
    room = data["room"]
    join_room(room)
    send("Joined room: " + room, room=room)
    print("Joined room: " + room)

@socketio.on("leave")
def handle_leave(data):
    room = data["room"]
    msg = data["msg"]
    leave_room(room)
    send("Left room: " + room, room=room)
    send(msg)
    print("Left room: " + room)

@socketio.on("join", namespace= "/chat")
def handle_join_chat(data):
    room = data["room"]
    join_room(room)
    send("Joined room: " + room, room=room)
    emit("message", {"data": "Joined room: " + room})
    print("Joined room: " + room)

@socketio.on("send_message_to_room")
def handle_send_message_to_room(data):
    room = data["room"]
    message = data["message"]
    send(message, room=room)
    print("Message sent to room: " + room)





if __name__ == "__main__":
    # make hot reloading 
    socketio.run(app, debug=True)
