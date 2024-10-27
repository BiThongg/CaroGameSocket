from typing import Dict, List

from jsonpickle.handlers import uuid
from User import User
from room.Room import Room


class Storage:
    def __init__(self) -> None:
        self.rooms: Dict[str, Room] = {}
        self.users: Dict[str, User] = {}

    def getRoom(self, roomId: str) -> Room | None:
        return self.rooms.get(roomId)

    def getUser(self, userId: str) -> User | None:
        return self.users.get(userId)

    def addRoom(self, room: Room) -> None:
        self.rooms[room.id] = room
        return

    def removeRoom(self, room: Room) -> None:
        self.rooms.pop(room.id)
        return

    def addUser(self, user: User) -> None:
        self.users[user.id] = user
        return

    def removeUser(self, user: User) -> None:
        self.users.pop(user.id)
        return

    def getRooms(self) -> List[Room]:
        return list(self.rooms.values())

    def getUsers(self) -> List[User]:
        return list(self.users.values())

    def createRoom(self, name: str, userId) -> Room:
        user = self.users.get(userId)
        if user is None:
            raise Exception("User not found")
        name = str(uuid.uuid4())

        room = Room(name=name, owner=user)
        self.addRoom(room)
        return room

    def getRoomByUserId(self, userId: str) -> Room | None:
        for room in self.rooms.values():
            if room.owner.info.id == userId:
                return room
        return None
