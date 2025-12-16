import math
from backend.game import winner, is_full, evaluate, heuristic_score

USE_ALPHABETA = True #Mặc định bật 
MAX_DEPTH = None

PLAYER = "X"
AI = "O" if PLAYER == "X" else "X"

def get_candidate_moves(board, radius=1):
    """
    Chỉ xét các ô trống nằm gần (trong vòng 'radius') những ô đã đánh
    để giảm số lượng nhánh cần duyệt ⇒ đỡ lag.
    """
    n = int(len(board) ** 0.5)
    occupied = [i for i, v in enumerate(board) if v != " "]

    # Nếu bàn trống hoàn toàn -> đánh ở giữa
    if not occupied:
        return [len(board) // 2]

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

    if not cand:
        # fallback: nếu vì lý do gì đó không có ô nào
        cand = {i for i, v in enumerate(board) if v == " "}

    return list(cand)


def minimax(board, depth, alpha, beta, is_maximizing,AI,PLAYER):
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
        for i in get_candidate_moves(board):
            board[i] = AI
            eval = minimax(board, depth + 1, alpha, beta, False, AI, PLAYER)
            board[i] = " "

            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)

            # 🔥 AI thắng chắc thì dừng
            if max_eval >= 1:
                return max_eval

            if beta <= alpha:
                break
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
        return min_eval

# minimax ko có alpha-beta
def minimax_noAB(board, is_maximizing, AI, PLAYER, depth=0):
    score = evaluate(board, AI, PLAYER)

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
    import math
    scored_moves = []

    # 1️⃣ Chấm điểm nhanh từng nước bằng heuristic
    for i in get_candidate_moves(board):
        if board[i] != " ":
            continue

        board[i] = AI
        h = heuristic_score(board, AI, PLAYER)
        board[i] = " "
        scored_moves.append((h, i))

    # 2️⃣ Duyệt nước tốt trước (RẤT QUAN TRỌNG)
    scored_moves.sort(reverse=True)

    best_score = -math.inf
    best_move = None

    # 3️⃣ Gọi minimax theo thứ tự đã sắp
    for _, i in scored_moves:
        board[i] = AI

        if USE_ALPHABETA:
            score = minimax(board, 0, -math.inf, math.inf, False, AI, PLAYER)
        else:
            score = minimax_noAB(board, False, AI, PLAYER, 0)

        board[i] = " "

        if score > best_score:
            best_score = score
            best_move = i

        # 4️⃣ CẮT SỚM nếu thắng chắc
        if best_score >= 1:
            break

    return best_move

