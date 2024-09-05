from abc import ABC, abstractmethod

# class Game():
#     def __init__(self, player1_id, player2_id):
#         self.id = str(uuid.uuid4())
#         self.winner = None
#         self.game_time = {
#             player1_id: str(datetime.now()),
#             player2_id: str(datetime.now())
#         }
#         self.start_at = str(datetime.now())
#         self.chess_board = CaroGame().board
#
#         def is_can_strike(self, id):
#             return self.game_time[id] != None
#

class Game(ABC):
    def __init__(self) -> None:
        pass
