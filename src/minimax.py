import math
from game import winner, is_full, evaluate

def minimax(board, depth, is_maximizing):
    score = evaluate(board)

    # Dừng nếu có kết quả hoặc hết ô
    if score != 0 or is_full(board):
        return score

    if is_maximizing:
        best_score = -math.inf
        for i in range(9):
            if board[i] == " ":
                board[i] = "O"
                value = minimax(board, depth + 1, False)
                board[i] = " "
                best_score = max(best_score, value)
        return best_score
    else:
        best_score = math.inf
        for i in range(9):
            if board[i] == " ":
                board[i] = "X"
                value = minimax(board, depth + 1, True)
                board[i] = " "
                best_score = min(best_score, value)
        return best_score


def best_move(board):
    """Tìm nước đi tốt nhất cho AI (O)"""
    best_score = -math.inf
    move = None
    for i in range(9):
        if board[i] == " ":
            board[i] = "O"
            score = minimax(board, 0, False)
            board[i] = " "
            if score > best_score:
                best_score = score
                move = i
    return move
