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

    # def check_end_game(self, direc, my_syl, current_point, start_point):
    #     if

    def is_end_game(self, id, position):
        player = self.game_detail[id]['value']
        x = position['y']
        y = position['x']

        directions = [
            (1, 0),   # Horizontal
            (0, 1),   # Vertical
            (1, 1),   # Diagonal (top-left to bottom-right)
            (1, -1)   # Diagonal (bottom-left to top-right)
        ]
        
        for dx, dy in directions:
            count = 1
            # Kiểm tra theo hướng dương
            i, j = x + dx, y + dy
            while 0 <= i < len(self.chess_board) and 0 <= j < len(self.chess_board[0]) and self.chess_board[i][j] == player:
                count += 1
                i += dx
                j += dy
                
            # Kiểm tra theo hướng ngược lại
            i, j = x - dx, y - dy
            while 0 <= i < len(self.chess_board) and 0 <= j < len(self.chess_board[0]) and self.chess_board[i][j] == player:
                count += 1
                i -= dx
                j -= dy
                
            if count >= 5:
                return True
                
        return False

    def is_can_strike(self, id, position):
        return self.game_detail[id] != None and self.chess_board[position['y'], position['x']] == 0.0
    
    def is_my_turn(self, id):
        competitor_id = self.game_detail[id]['competitor_id']
        print(self.game_detail[id]['latest_time'] <= self.game_detail[competitor_id]['latest_time'])
        return self.game_detail[id]['latest_time'] <= self.game_detail[competitor_id]['latest_time']
    
    def mark(self, id, position):
        self.chess_board[position['y'], position['x']] = self.game_detail[id]['value']

    def validiate_time_limit_set_latest_time_and(self, id):
        competitor_id = self.game_detail[id]['competitor_id']
        time_consuming = datetime.now() - datetime.strptime(self.game_detail[competitor_id]['latest_time'], "%Y-%m-%d %H:%M:%S.%f")
        if int(time_consuming.total_seconds()) > 50:
            return False
        self.game_detail[id]['latest_time'] = str(datetime.now())
        return True