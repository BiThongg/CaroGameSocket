import uuid


class User:
    def __init__(self, name: str, id: str = uuid.uuid4().__str__()):
        self.name = name
        self.id = id

    def serialize(self):
        return {"id": self.id, "name": self.name}
