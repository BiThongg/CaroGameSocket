from room import Room
from user import User


class RoomDTO:
    def __init__(self):
        pass

    def to_dict(room: Room):
        return {"id": room.id, "name": room.name}

    def to_dto(room: Room):
        return {"id": room.id, "name": room.name, "owner": User.to_dto(room.owner)}
