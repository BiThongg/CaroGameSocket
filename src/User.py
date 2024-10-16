import uuid


class User:
    def __init__(self, name: str, id: str):
        self.id = id
        self.name = name
        self.currentToken = None
        self.storageId = str(uuid.uuid4())

    def serialize(self):
        return {"name": self.name, "id": self.id}
