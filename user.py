class User():
    def __init__(self, id, name):
        self.id = str(id)
        self.name = name
        # self.room_played = []
        # self.latest_room = None # In case until in game play if guest/lead suddenly out game, we can rely on this value to continue game