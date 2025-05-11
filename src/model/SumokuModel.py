import time
from util.cell import Cell


class CaroModel:
    board = []
    start = time.time()

    time_limit = 6

    def __init__(self):
        pass

    # test
    def actions(self, board):
        possible_actions = set()

        for i in range(board.__len__()):
            for j in range(board[i].__len__()):
                if board[j][i] == Cell.NONE:
                    possible_actions.add((j, i))

        return possible_actions

    def result(self, board, action):
        if action not in self.actions(board):
            raise Exception("Invalid action")

        new_board = [row[:] for row in board]

        new_board[action[0]][action[1]] = self.player(board)

        return new_board

    def player(self, board):
        """
        Returns player who has the next turn on a board.
        """

        x_count = 0
        o_count = 0

        for i in range(board.__len__()):
            for j in range(board[i].__len__()):
                if board[j][i] == Cell.X:
                    x_count += 1
                elif board[j][i] == Cell.O:
                    o_count += 1

        if x_count > o_count:
            return Cell.O
        else:
            return Cell.X

    def terminal(self, board):
        if self.winner(board) is not None:
            return True

        for i in range(board.__len__()):
            for j in range(board[i].__len__()):
                if board[j][i] == Cell.NONE:
                    return False

        return True

    def winner(self, board):
        _size = board.__len__()
        for i in range(_size):
            for j in range(_size):
                if board[i][j] != Cell.NONE:
                    # check horizontal
                    if j < _size - 4:
                        if (
                            board[i][j]
                            == board[i][j + 1]
                            == board[i][j + 2]
                            == board[i][j + 3]
                            == board[i][j + 4]
                        ):
                            return board[i][j]
                    # check vertical
                    if i < _size - 4:
                        if (
                            board[i][j]
                            == board[i + 1][j]
                            == board[i + 2][j]
                            == board[i + 3][j]
                            == board[i + 4][j]
                        ):
                            return board[i][j]
                    # check diagonal
                    if i < _size - 4 and j < _size - 4:
                        if (
                            board[i][j]
                            == board[i + 1][j + 1]
                            == board[i + 2][j + 2]
                            == board[i + 3][j + 3]
                            == board[i + 4][j + 4]
                        ):
                            return board[i][j]
                    if i < _size - 4 and j > 4:
                        if (
                            board[i][j]
                            == board[i + 1][j - 1]
                            == board[i + 2][j - 2]
                            == board[i + 3][j - 3]
                            == board[i + 4][j - 4]
                        ):
                            return board[i][j]

                    return None

    def utility(self, board):
        if self.winner(board) == Cell.X:
            return 1
        elif self.winner(board) == Cell.O:
            return -1
        else:
            return 0

    def minimax(self, board):
        if self.terminal(board):
            return self.utility(board)

        if self.player(board) == Cell.X:
            return self.max_alpha_beta(-2, 2)
        return 1

    def max_alpha_beta(self, alpha, beta, board, depth=0):
        # Check if the game has reached a terminal state
        result = self.terminal(board)
        if result:
            winner = self.winner(board)
            if winner == Cell.X:
                return (1, None, None)  # X wins
            elif winner == Cell.O:
                return (-1, None, None)  # O wins
            else:
                return (0, None, None)  # Draw

        maxv = -float("inf")
        px = py = None

        start_time = time.time()

        for action in self.actions(board):
            (i, j) = action

            # Time limit check
            if (time.time() - start_time) > self.time_limit:
                return (maxv, px, py)

            # Simulate the move for player X (maximizer)
            board[i][j] = Cell.X
            (m, _, _) = self.min_alpha_beta(alpha, beta, board, depth + 1)
            board[i][j] = Cell.NONE  # Undo move

            if m > maxv:
                maxv = m
                px = i
                py = j

            if maxv >= beta:
                return (maxv, px, py)  # Beta cutoff (pruning)

            alpha = max(alpha, maxv)

        return (maxv, px, py)

    def min_alpha_beta(self, alpha, beta, board, depth=0):
        # Check if the game has reached a terminal state
        result = self.terminal(board)
        if result:
            winner = self.winner(board)
            if winner == Cell.X:
                return (1, None, None)  # X wins
            elif winner == Cell.O:
                return (-1, None, None)  # O wins
            else:
                return (0, None, None)  # Draw

        minv = float("inf")
        qx = qy = None

        start_time = time.time()

        for action in self.actions(board):
            (i, j) = action

            # Time limit check
            if (time.time() - start_time) > self.time_limit:
                return (minv, qx, qy)

            # Simulate the move for player O (minimizer)
            board[i][j] = Cell.O
            (m, _, _) = self.max_alpha_beta(alpha, beta, board, depth + 1)
            board[i][j] = Cell.NONE  # Undo move

            if m < minv:
                minv = m
                qx = i
                qy = j

            if minv <= alpha:
                return (minv, qx, qy)  # Alpha cutoff (pruning)

            beta = min(beta, minv)

        return (minv, qx, qy)
