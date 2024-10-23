from flask_cors import CORS
<<<<<<< HEAD
from flask import Flask
=======
from flask import Flask, request
>>>>>>> f6484a2170598a6470c0116c69374ce7cce08a1c
from flask_socketio import SocketIO

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*")
<<<<<<< HEAD

=======
>>>>>>> f6484a2170598a6470c0116c69374ce7cce08a1c
