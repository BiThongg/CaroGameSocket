import numpy as np

from flask_cors import CORS
from flask import Flask, json, request
from flask_socketio import SocketIO, emit


app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*")



@socketio.on("connect")
def connect():
    print("heelo", request.sid)


@socketio.on("disconnect")
def disconnect():
    print(">> client {} disconnected to server".format(request.sid))



if __name__ == "__main__":
    socketio.run(app, debug=False)
