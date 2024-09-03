import uuid
import numpy as np
from datetime import datetime

class Game():
    def __init__(self, player1_id, player2_id):
        self.id = str(uuid.uuid4())
        self.room_id = None
        self.start_at = str(datetime.now())
        self.winner = None
        self.game_detail = {
            player1_id: {
                'value': 1,
                'latest_time': str(datetime.now()),
                'competitor_id': player2_id
            },
            player2_id: {
                'value': 2,
                'latest_time': str(datetime.now()),
                'competitor_id': player1_id
            }
        }
        self.chess_board = np.zeros((15, 15))

    def is_end_game(self):
        return False

    def is_can_strike(self, id):
        return self.game_detail[id] != None
    
    def is_my_turn(self, id):
        competitor_id = self.game_detail[id]['competitor_id']
        return self.game_detail[id]['latest_time'] <= self.game_detail[competitor_id]['latest_time']
    
    def mark(self, id, position):
        self.chess_board[position['y'], position['x']] = self.game_detail[id]['value']

    def validiate_time_limit_set_latest_time_and(self, id):
        competitor_id = self.game_detail[id]['competitor_id']
        time_consuming = datetime.now() - datetime.strptime(self.game_detail[competitor_id]['latest_time'], "%Y-%m-%d %H:%M:%S")
        if time_consuming.total_seconds() > 20:
            return False
        self.game_detail[id]['latest_time'] = str(datetime.now())
        return True