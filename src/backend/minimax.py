import math
from backend.game import winner, is_full, evaluate

USE_ALPHABETA = True #Mặc định bật 
MAX_DEPTH = None

PLAYER = "X"
AI = "O" if PLAYER == "X" else "X"

def minimax(board, depth, alpha, beta, is_maximizing,AI,PLAYER):
    score = evaluate(board,AI,PLAYER)

    # Dừng khi có kết quả, hết ô trống, hoặc đạt độ sâu tối đa
    if score != 0 or is_full(board) or (MAX_DEPTH is not None and depth >= MAX_DEPTH):
        return score

    if is_maximizing:  
        # Lượt của AI (O)
        max_eval = -math.inf
        for i in range(9):
            if board[i] == " ":
                board[i] = AI
                eval = minimax(board, depth + 1, alpha, beta, False,AI,PLAYER)
                board[i] = " "
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  # Cắt tỉa Beta
        return max_eval
    else:  
        # Lượt của người chơi (X)
        min_eval = math.inf
        for i in range(9):
            if board[i] == " ":
                board[i] = PLAYER
                eval = minimax(board, depth + 1, alpha, beta, True,AI,PLAYER)
                board[i] = " "
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break  # Cắt tỉa Alpha
        return min_eval

# minimax ko có alpha-beta
def minimax_noAB(board, is_maximizing, AI, PLAYER, depth=0):
    score = evaluate(board, AI, PLAYER)

    if score != 0 or is_full(board) or (MAX_DEPTH is not None and depth >= MAX_DEPTH):
        return score

    if is_maximizing:
        best = -math.inf
        for i in range(9):
            if board[i] == " ":
                board[i] = AI
                val = minimax_noAB(board, False, AI, PLAYER, depth + 1)
                board[i] = " "
                best = max(best, val)
        return best
    else:
        best = math.inf
        for i in range(9):
            if board[i] == " ":
                board[i] = PLAYER
                val = minimax_noAB(board, True, AI, PLAYER, depth + 1)
                board[i] = " "
                best = min(best, val)
        return best

def best_move(board,AI,PLAYER):
    """Tìm nước đi tốt nhất cho AI (O) bằng Minimax + Alpha-Beta"""
    best_score = -math.inf
    move = None

    for i in range(9):
        if board[i] == " ":
            board[i] = AI
            
            if USE_ALPHABETA:
               score = minimax(board, 0, -math.inf, math.inf, False, AI, PLAYER)
            else:
               score = minimax_noAB(board, False, AI, PLAYER, 0)
               
            board[i] = " "
            
            if score > best_score:
                best_score = score
                move = i

    return move
