import math
from backend.game import winner, is_full, evaluate, heuristic_score, WIN_LENGTH
TRANSPOSITION = {}
USE_ALPHABETA = True #Mặc định bật 
MAX_DEPTH = None

NODES_VISITED = 0

PLAYER = "X"
AI = "O" if PLAYER == "X" else "X"

def get_candidate_moves(board):
    n = int(len(board) ** 0.5)
    occupied = [i for i, v in enumerate(board) if v != " "]

    # Nếu bàn trống hoàn toàn → đánh giữa
    if not occupied:
        return [len(board) // 2]

    # 🔥 radius phụ thuộc độ dài thắng
    radius = max(1, WIN_LENGTH - 2)

    cand = set()
    for idx in occupied:
        r = idx // n
        c = idx % n

        for dr in range(-radius, radius + 1):
            for dc in range(-radius, radius + 1):
                rr = r + dr
                cc = c + dc
                if 0 <= rr < n and 0 <= cc < n:
                    j = rr * n + cc
                    if board[j] == " ":
                        cand.add(j)

    return list(cand)


def minimax(board, depth, alpha, beta, is_maximizing,AI,PLAYER):
    key = (tuple(board), depth, is_maximizing)
    if key in TRANSPOSITION:
        return TRANSPOSITION[key]
    global NODES_VISITED
    NODES_VISITED += 1
    score = evaluate(board, AI, PLAYER)

    # Nếu đã thắng / thua / hòa -> trả về ngay
    if score != 0 or is_full(board):
        return score

    # Nếu đạt độ sâu tối đa nhưng chưa endgame -> dùng heuristic
    if MAX_DEPTH is not None and depth >= MAX_DEPTH:
        return heuristic_score(board, AI, PLAYER)

    if is_maximizing:  
        # Lượt của AI
        max_eval = -math.inf
        moves = get_candidate_moves(board)
        if depth == 0:
            moves.sort(
                key=lambda i: heuristic_score(
                    board[:i] + [AI] + board[i+1:], AI, PLAYER
                ),
                reverse=True
            )
            moves = moves[: max(4, WIN_LENGTH + 1)]
            

        for i in moves:
            board[i] = AI
            eval = minimax(board, depth + 1, alpha, beta, False, AI, PLAYER)
            board[i] = " "

            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)

            # 🔥 AI thắng chắc thì dừng
            if max_eval ==1:
                return 1

            if beta <= alpha:
                break
        TRANSPOSITION[key] = max_eval
        return max_eval

    else:  
        # Lượt của người chơi
        min_eval = math.inf
        for i in get_candidate_moves(board):
            board[i] = PLAYER
            eval = minimax(board, depth + 1, alpha, beta, True, AI, PLAYER)
            board[i] = " "
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break  # Cắt tỉa Alpha
        TRANSPOSITION[key] = min_eval
        return min_eval

# minimax ko có alpha-beta
def minimax_noAB(board, is_maximizing, AI, PLAYER, depth=0):
    score = evaluate(board, AI, PLAYER)
    global NODES_VISITED
    NODES_VISITED += 1

    if score != 0 or is_full(board):
        return score
    if MAX_DEPTH is not None and depth >= MAX_DEPTH:
        return heuristic_score(board, AI, PLAYER)

    if is_maximizing:
        best = -math.inf
        for i in get_candidate_moves(board):
            if board[i] == " ":
                board[i] = AI
                val = minimax_noAB(board, False, AI, PLAYER, depth + 1)
                board[i] = " "
                best = max(best, val)
        return best
    else:
        best = math.inf
        for i in get_candidate_moves(board):
            if board[i] == " ":
                board[i] = PLAYER
                val = minimax_noAB(board, True, AI, PLAYER, depth + 1)
                board[i] = " "
                best = min(best, val)
        return best

def best_move(board, AI, PLAYER):

    # 1️⃣ AI thắng ngay
    for i in get_candidate_moves(board):
        board[i] = AI
        if winner(board, AI):
            board[i] = " "
            return i
        board[i] = " "

    # 2️⃣ BLOCK nếu player sắp thắng
    for i in get_candidate_moves(board):
        board[i] = PLAYER
        if winner(board, PLAYER):
            board[i] = " "
            return i
        board[i] = " "

    # 3️⃣ Nếu không có tình huống đặc biệt → minimax
    best_score = -math.inf
    best = None

    for i in get_candidate_moves(board):
        board[i] = AI
        if USE_ALPHABETA:
            score = minimax(board, 0, -math.inf, math.inf, False, AI, PLAYER)
        else:
            score = minimax_noAB(board, False, AI, PLAYER, 0)

        board[i] = " "

        if score > best_score:
            best_score = score
            best = i

    return best

