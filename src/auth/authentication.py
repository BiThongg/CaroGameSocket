from flask_socketio import Namespace, emit
from flask import Flask, session, request
import jwt
import json
from datetime import datetime, timedelta
from functools import wraps
from database.data import storage

SECRET_KEY = 'your_jwt_secret_key'

def decode_jwt(token: str) -> dict[str, str]:
    try:
        payload: dict[str, str] = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    
def encode_jwt(userId: str) -> str:
    payload = {
        'sub': userId,
        'exp': datetime.now() + timedelta(hours=1)
    }
    token: str = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

# def request_access(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         token: str = request.headers.get('x-auth-token')
#         userId: str = decode_jwt(token)['user_id']
        
#         if userId is None or userId != request.sid:
#             userId = decode_jwt(token)['user_id']
#             user = storage.users.pop(userId)
#             if user is None:
#                 raise Exception("Not found user")
#             user.id = request.sid
#             storage.users[user.id] = user
#             token = encode_jwt(user.id)
#         else:
#             user = User(id=request.sid, name=name_generation(5))
#             storage.users[user.id] = user
#             token = encode_jwt(user.id)
#             return f(*args, **kwargs)
#     return decorated_function
    
def authentication_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        data: dict = args[0] if args else {}
        currentToken: str = data.get('token', None)
        userId: str = decode_jwt(currentToken)['sub']
        
        if currentToken != storage.getUser(userId=userId).currentToken:
            raise Exception("Not found user")
        
        if storage.getUser(userId=userId).id != request.sid:
            raise Exception("Unauthen, Error token")
        
        message: dict = data.get('message', None)
        return f(message)
    return decorated_function

# def requires_authentication(f):
#     def wrapper(*args, **kwargs):
#         token = request.headers.get("x-authentication-token")
#         if not token:
#             emit(
#                 "data_fetched",
#                 "token is missing",
#                 to=request.sid
#             )
#         payload = verify_token(token)
#         if not payload:
#             emit(
#                 "data_fetched",
#                 "token is expired",
#                 to=request.sid
#             )
#         if payload.lastest_session_id != storage.getUser(payload.sub):
#             emit(
#                 "data_fetched",
#                 "token is expired",
#                 to=request.sid
#             )
        
#         return f(*args, **kwargs)
#     return wrapper
