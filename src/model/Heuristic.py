from util.cell import Cell
import re

class Heuristic:
    def __init__(self):
        self.eval_board = [[0 for _ in range(14)] for _ in range(14)]

    replace_cell = {Cell.X: 1, Cell.O: 2, Cell.NONE: 0}

    opponent_player = {Cell.X: Cell.O, Cell.O: Cell.X}

    # PATTERN MATCHING
    case_user = [
        "11001", "10101", "10011",
        "00110", "01010", "01100",
        "11100", "11010", "10110", "01101", "01011", "00111",
        "01110",
        "011100", "011010", "010110", "001110", "1010101", "1011001", "1001101",
        "01111", "10111", "11011", "11101", "11101", "11110",
        "11111"
    ]

    case_ai = [
        "22002", "20202", "20022",
        "00220", "02020", "02200",
        "22200", "22020", "20220", "02202", "02022", "00222",
        "02220",
        "022200", "022020", "020220", "002220", "2020202", "2022002", "2002202",
        "02222", "20222", "22022", "22202", "22202", "22220",
        "22222"
    ]

    point = [
        4, 4, 4,
        8, 8, 8,
        8, 8, 8, 8, 8, 8,
        8,
        500, 500, 500, 500, 500, 500, 500,
        1000, 1000, 1000, 1000, 1000, 1000,
        100000
    ]

    # Trích xuất tất cả các dòng (ngang, dọc, chéo chính, chéo phụ) từ bàn cờ thành một chuỗi
    def extract_all_lines(self, board):
        res = ";"
        size = len(board)

        # Đường ngang __ và dọc |
        for i in range(size):
            res += ''.join(str(self.replace_cell[board[i][j]]) for j in range(size)) + ";"
            res += ''.join(str(self.replace_cell[board[j][i]]) for j in range(size)) + ";"

        # Đường chéo chính (\) - nửa trên
        for i in range(size - 4):
            res += ''.join(str(self.replace_cell[board[j][i + j]]) for j in range(size - i)) + ";"

        # Đường chéo chính (\) - nửa dưới
        for i in range(size - 5, 0, -1):
            res += ''.join(str(self.replace_cell[board[i + j][j]]) for j in range(size - i)) + ";"

        # Đường chéo phụ (/) - nửa trên
        for i in range(4, size):
            res += ''.join(str(self.replace_cell[board[i - j][j]]) for j in range(i + 1)) + ";"

        # Đường chéo phụ (/) - nửa dưới
        for i in range(size - 5, 0, -1):
            res += ''.join(str(self.replace_cell[board[j][i + size - j - 1]]) for j in range(size - 1, i - 1, -1)) + ";"

        return res   

    # Đếm số lần xuất hiện của một mẫu (pattern) trong chuỗi
    def count_occurrences(self, text, pattern):
        return len(re.findall(pattern, text))

    # Đánh giá điểm toàn bộ bàn cờ dựa trên các mẫu (pattern)
    def evaluate_board(self, board):
        lines = self.extract_all_lines(board)
        total_score = 0
        for i in range(len(self.case_user)):
            pattern_user = self.case_user[i]
            pattern_ai = self.case_ai[i]
            pattern_point = self.point[i]

            # Cộng điểm nếu là pattern của AI và trừ điểm nếu là pattern của người chơi
            total_score += pattern_point * self.count_occurrences(lines, pattern_ai)
            total_score -= pattern_point * self.count_occurrences(lines, pattern_user)

        # Nếu điểm lớn hơn 0, AI đang có lợi thế và ngược lại
        return total_score  

    # ATTACKING AND DEFENSE SCORE
    defense_score = [0, 1, 9, 81, 729, 6534]
    attack_score = [0, 3, 24, 192, 1536, 12288]

    # Đặt lại bảng đánh giá về giá trị 0
    def reset_eval_board(self):
        for i in range(14):
            for j in range(14):
                self.eval_board[i][j] = 0

    # Đánh giá từng ô trên bàn cờ dựa trên người chơi (player)
    def evaluate_each_cell(self, board, player):
        size = len(board)
        self.reset_eval_board()

        # Hàng ngang 
        for y in range(size):
            for x in range(size - 4):
                # Đếm số ô của AI (O) trong 5 ô liên tiếp
                count_ai = sum(1 for i in range(5) if board[y][x + i] == Cell.O)
                # Đếm số ô của người chơi (X) trong 5 ô liên tiếp
                count_user = sum(1 for i in range(5) if board[y][x + i] == Cell.X)

                # Chỉ tính điểm khi không có cả X và O trong cùng một dòng, tức là chỉ có một loại ô + các ô trống
                if count_ai * count_user == 0 and count_ai != count_user:
                    for i in range(5):
                        if board[y][x + i] == Cell.NONE:
                            # Tính điểm phòng thủ hoặc tấn công dựa trên người chơi
                            if count_ai == 0:
                                score = self.defense_score[count_user] if player == Cell.O else self.attack_score[count_user]
                                self.eval_board[y][x + i] += score
                            elif count_user == 0:
                                score = self.defense_score[count_ai] if player == Cell.X else self.attack_score[count_ai]
                                self.eval_board[y][x + i] += score
                            
                            # Nhân đôi điểm nếu có 4 ô liên tiếp (gần thắng)
                            if count_ai == 4 or count_user == 4:
                                self.eval_board[y][x + i] *= 2  

        # Hàng dọc 
        for x in range(size):
            for y in range(size - 4):
                count_ai = sum(1 for i in range(5) if board[y + i][x] == Cell.O)
                count_user = sum(1 for i in range(5) if board[y + i][x] == Cell.X)

                if count_ai * count_user == 0 and count_ai != count_user:
                    for i in range(5):
                        if board[y + i][x] == Cell.NONE:
                            if count_ai == 0:
                                self.eval_board[y + i][x] += (
                                    self.defense_score[count_user] if player == Cell.O else self.attack_score[count_user]
                                )
                            elif count_user == 0:
                                self.eval_board[y + i][x] += (
                                    self.defense_score[count_ai] if player == Cell.X else self.attack_score[count_ai]
                                )
                            if count_ai == 4 or count_user == 4:
                                self.eval_board[y + i][x] *= 2

        # Đường chéo chính
        for y in range(size - 4):
            for x in range(size - 4):
                count_ai = sum(1 for i in range(5) if board[y + i][x + i] == Cell.O)
                count_user = sum(1 for i in range(5) if board[y + i][x + i] == Cell.X)

                if count_ai * count_user == 0 and count_ai != count_user:
                    for i in range(5):
                        if board[y + i][x + i] == Cell.NONE:
                            if count_ai == 0:
                                self.eval_board[y + i][x + i] += (
                                    self.defense_score[count_user] if player == Cell.O else self.attack_score[count_user]
                                )
                            elif count_user == 0:
                                self.eval_board[y + i][x + i] += (
                                    self.defense_score[count_ai] if player == Cell.X else self.attack_score[count_ai]
                                )
                            if count_ai == 4 or count_user == 4:
                                self.eval_board[y + i][x + i] *= 2

        # Đường chéo phụ
        for y in range(4, size):
            for x in range(size - 4):
                count_ai = sum(1 for i in range(5) if board[y - i][x + i] == Cell.O)
                count_user = sum(1 for i in range(5) if board[y - i][x + i] == Cell.X)

                if count_ai * count_user == 0 and count_ai != count_user:
                    for i in range(5):
                        if board[y - i][x + i] == Cell.NONE:
                            if count_ai == 0:
                                self.eval_board[y - i][x + i] += (
                                    self.defense_score[count_user] if player == Cell.O else self.attack_score[count_user]
                                )
                            elif count_user == 0:
                                self.eval_board[y - i][x + i] += (
                                    self.defense_score[count_ai] if player == Cell.X else self.attack_score[count_ai]
                                )
                            if count_ai == 4 or count_user == 4:
                                self.eval_board[y - i][x + i] *= 2

    # Lấy giá trị đánh giá của ô tại vị trí (y, x)
    def get_eval_cell_value(self, y, x):
        return self.eval_board[y][x]  

    # Tính độ dài của số (số chữ số)
    def length_num(self, n):
        return len(str(abs(int(n)))) if n != float('-inf') else 1

    # Lấy danh sách tối đa các ô có điểm số cao nhất (max = 8 ô)
    def get_optimal_list(self):
        size = 8
        max_value_list = [float('-inf')] * size
        max_cell_list = [(-1, -1) for _ in range(size)]  # (y, x)

        board_size = len(self.eval_board)

        for y in range(board_size):
            for x in range(board_size):
                value = self.get_eval_cell_value(y, x)
                if value == 0:
                    continue

                # Chèn giá trị và tọa độ ô vào danh sách theo thứ tự giảm dần
                for i in reversed(range(size)):
                    if max_value_list[i] <= value:
                        # Dời các phần tử về trước để nhường chỗ
                        for j in range(i):
                            max_value_list[j] = max_value_list[j + 1]
                            max_cell_list[j] = max_cell_list[j + 1]
                        # Gán giá trị vào vị trí đúng
                        max_value_list[i] = value
                        max_cell_list[i] = (y, x)
                        break

        # Lọc các ô gần với điểm cao nhất
        max_length = self.length_num(max_value_list[-1])
        difference = [0, 2, 8, 32, 128, 512]

        result = [max_cell_list[-1]]  # phần tử có điểm lớn nhất
        for i in reversed(range(size - 1)):
            if max_value_list[-1] - max_value_list[i] <= difference[max_length]:
                result.append(max_cell_list[i])
            else:
                break

        return result









    


