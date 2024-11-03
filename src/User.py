import uuid


class User:
    def __init__(self, name: str, sid: str | None):
        self.id  = str(uuid.uuid4()) 
        self.sid = sid
        self.name = name
        
    def serialize(self):
        return {"name": self.name, "id": self.id}
