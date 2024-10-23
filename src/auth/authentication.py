from database.data import storage
from flask import request
import jwt
from datetime import datetime, timedelta
from functools import wraps

SECRET_KEY = "WINNGUYEN1905"


def decode_jwt(token: str) -> dict[str, str]:
    try:
        payload: dict[str, str] = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def encode_jwt(userId: str) -> str:
    payload = {"sub": userId, "exp": datetime.now() + timedelta(hours=1)}
    token: str = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


def user_infomation_filter(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        payload: dict = args[0] if args else {}
        print(payload.get("user_id") or request.args.get("user_id") or "None")

        userId: str = request.args.get("user_id") or payload.get("user_id")
        user = storage.getUser(userId) if userId != None else None
        return f(user, payload)

    return decorated_function


def authentication_required_filter(f):
    @wraps(f)
    def decorated_function(*args):
        # START HANDLE FOR JWT
        data: dict = args[0] if args else {}
        currentToken: str = data.get("token", None)
        userId: str = decode_jwt(currentToken)["sub"]
        if currentToken != storage.getUser(userId=userId).token:
            raise Exception("Not found user")
        if storage.getUser(userId=userId).sid != request.sid:
            raise Exception("Unauthen, Error token")
        # START HANDLE FOR JWT
        message: dict = data.get("message", None)
        return f(userId, message)

    return decorated_function
