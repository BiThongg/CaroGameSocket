from player.Player import Player
from User import User


class PersonPlayer(Player):
    def __init__(self, user: User):
        super().__init__(user)
        return
