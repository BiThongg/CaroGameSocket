from util.cell import Cell
from model.Heuristic import Heuristic
import random

class SumokuAI:
    def __init__(self):
        self.heuristic = Heuristic()
        self.MAX_DEPTH = 4 # Độ sâu tối đa 
        self.opponent_player = {Cell.X: Cell.O, Cell.O: Cell.X}
    
    # Thuật toán alpha-beta để tìm nước đi tối ưu cho người chơi
    def alpha_beta(self, board, player):

        # Gọi hàm đánh giá điểm số cho từng ô trên bàn cờ 
        self.heuristic.evaluate_each_cell(board, player)

        # Lấy danh sách các ô có điểm số cao nhất
        ls = self.heuristic.get_optimal_list()

        # Lưu trữ giá trị lớn nhất (-inf)
        _max = float('-inf')

        # Lưu danh sách các ô có điểm số lớn nhất 
        ls_choose = []
    
        # Duyệt qua từng ô trong danh sách tối ưu
        for y, x in ls:
            board[y][x] = player  # Giả sử AI đánh vào ô này

            # Gọi đệ quy xuống min_value để mô phỏng phản ứng của người chơi, trả về điểm số tương ứng
            _value = self.min_value(board, float('-inf'), float('inf'), 0, self.opponent_player[player]) 

            # Nếu giá trị lớn hơn giá trị lớn nhất hiện tại, cập nhật giá trị lớn nhất và danh sách các ô
            if _max < _value:
                _max = _value
                ls_choose.clear()
                ls_choose.append((y, x))
            elif _max == _value: 
                ls_choose.append((y, x))
            board[y][x] = Cell.NONE # Hoàn tác nước đi

        # Chọn ngẫu nhiên một nước đi từ danh sách các nước lớn nhất (bằng nhau)
        return random.choice(ls_choose)

    # Hàm tính giá trị nhỏ nhất trong thuật toán alpha-beta
    # Được gọi khi giả lập nước đi của người chơi muốn giảm điểm số của AI
    def min_value(self, board, alpha, beta, depth, player):

        # Kiểm tra điều kiện dừng: độ sâu tối đa, có người thắng, hoặc bàn cờ đầy
        if depth >= self.MAX_DEPTH or self.check_winner(board, self.opponent_player[player]) or self.is_over(board):
            return self.heuristic.evaluate_board(board) # Đánh giá điểm của toàn bộ bàn cờ 

        # Đánh giá điểm số cho từng ô trên bàn cờ
        self.heuristic.evaluate_each_cell(board, self.opponent_player[player])

        # Lấy danh sách các ô có điểm số cao nhất
        ls = self.heuristic.get_optimal_list() 

        # Duyệt qua từng ô trong danh sách
        for y, x in ls:
            board[y][x] = self.opponent_player[player] # Giả sử người chơi đánh vào ô này   

            # Gọi đệ quy xuống max_value để mô phỏng lượt đi của AI, sau đó lấy min trong các giá trị trả về để cập nhật điểm tốt nhất cho người chơi.
            beta = min(beta, self.max_value(board, alpha, beta, depth + 1, player))

            board[y][x] = Cell.NONE # Hoàn tác nước đi

            # Alpha (điểm tốt nhất của Max) đã lớn hn hoặc bằng Beta (điểm tốt nhất hiện tại của Min),
            # Max đã có lựa chọn tốt hơn ở nhánh kháơc nên không cần xét tiếp các lựa chọn còn lại của Min,
            if alpha >= beta:
                break # Cắt tỉa nhánh (pruning)
        
        return beta
    
    # Hàm tính giá trị lớn nhất trong thuật toán alpha-beta
    # Được gọi khi giả lập nước đi AI muốn tăng điểm số của mình
    def max_value(self, board, alpha, beta, depth, player):
        # Kiểm tra điều kiện dừng: độ sâu tối đa, có người thắng, hoặc bàn cờ đầy
        if depth >= self.MAX_DEPTH or self.check_winner(board, player) or self.is_over(board):
            return self.heuristic.evaluate_board(board) # Đánh giá điểm của toàn bộ bàn cờ 
        
        # Đánh giá điểm số cho từng ô trên bàn cờ
        self.heuristic.evaluate_each_cell(board, player)

        # Lấy danh sách các ô có điểm số cao nhất
        ls = self.heuristic.get_optimal_list()

        # Duyệt qua từng ô trong danh sách tối ưu
        for y, x in ls:
            board[y][x] = player # Giả sử AI đánh vào ô này

            # Gọi đệ quy xuống min_value để mô phỏng lượt đi của người chơi, sau đó lấy max trong các giá trị trả về để cập nhật điểm tốt nhất cho AI.
            alpha = max(alpha, self.min_value(board, alpha, beta, depth + 1, self.opponent_player[player]))
            
            board[y][x] = Cell.NONE # Hoàn tác nước đi
            
            # Alpha (điểm tốt nhất của Max) đã lớn hơn hoặc bằng Beta (điểm tốt nhất hiện tại của Min),
            # Max đã có lựa chọn tốt hơn ở nhánh khác nên không cần xét tiếp các lựa chọn còn lại của Min,
            if alpha >= beta:     
                break # Cắt tỉa nhánh (pruning)
        
        return alpha    

    # Kiểm tra xem bàn cờ có còn ô trống hay không
    def is_over(self, board):
        for y in range(len(board)):
            for x in range(len(board[y])):
                if board[y][x] == Cell.NONE:
                    return False
        return True

    # Kiểm tra xem người chơi đã thắng hay không
    def check_winner(self, board, player):
        size = len(board)
        directions = [(1, 0), (1, 1), (0, 1), (-1, 1)]  # (dy, dx): ↓, ↘, →, ↗

        for y in range(size):     
            for x in range(size):   
                if board[y][x] != player:
                    continue
                
                # Kiểm tra từng hướng
                for dy, dx in directions:
                    count = 1
                    for k in range(1, 5):
                        ny = y + dy * k
                        nx = x + dx * k

                        if 0 <= ny < size and 0 <= nx < size and board[ny][nx] == player:
                            count += 1
                        else:
                            break
                    
                    # Nếu có 5 ô liên tiếp, người chơi thắng
                    if count == 5:
                        return True

        return False


    