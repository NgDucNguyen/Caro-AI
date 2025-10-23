import math
from game import winner, is_full, evaluate

def minimax(board, depth, alpha, beta, is_maximizing):
    """Thuật toán Minimax có cắt tỉa Alpha-Beta"""
    score = evaluate(board)

    # Dừng khi có kết quả hoặc hết ô trống
    if score != 0 or is_full(board):
        return score

    if is_maximizing:  # Lượt của AI (O)
        max_eval = -math.inf
        for i in range(9):
            if board[i] == " ":
                board[i] = "O"
                eval = minimax(board, depth + 1, alpha, beta, False)
                board[i] = " "
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  # Cắt tỉa Beta
        return max_eval
    else:  # Lượt của người chơi (X)
        min_eval = math.inf
        for i in range(9):
            if board[i] == " ":
                board[i] = "X"
                eval = minimax(board, depth + 1, alpha, beta, True)
                board[i] = " "
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break  # Cắt tỉa Alpha
        return min_eval


def best_move(board):
    """Tìm nước đi tốt nhất cho AI (O) bằng Minimax + Alpha-Beta"""
    best_score = -math.inf
    move = None

    for i in range(9):
        if board[i] == " ":
            board[i] = "O"
            score = minimax(board, 0, -math.inf, math.inf, False)
            board[i] = " "
            if score > best_score:
                best_score = score
                move = i

    return move
