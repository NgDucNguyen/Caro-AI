# --- Các hàm xử lý bàn cờ Tic Tac Toe ---
BOARD_N = 3
WIN_LENGTH = 3

def set_board_params(n,winlen):
    global BOARD_N,WIN_LENGTH
    BOARD_N = n
    WIN_LENGTH = winlen

def winner(b, player):
    """Kiểm tra người thắng"""
    n = BOARD_N
    k = WIN_LENGTH
    
    # helper lấy index 1D từ (r, c)
    def idx(r, c):
        return r * n + c

    directions = [
        (1, 0),   # dọc xuống
        (0, 1),   # ngang phải
        (1, 1),   # chéo xuống phải
        (1, -1),  # chéo xuống trái
    ]

    for r in range(n):
        for c in range(n):
            if b[idx(r, c)] != player:
                continue

            for dr, dc in directions:
                # Kiểm tra điểm kết thúc có nằm trong bàn không
                end_r = r + (k - 1) * dr
                end_c = c + (k - 1) * dc
                if not (0 <= end_r < n and 0 <= end_c < n):
                    continue

                ok = True
                for step in range(k):
                    rr = r + step * dr
                    cc = c + step * dc
                    if b[idx(rr, cc)] != player:
                        ok = False
                        break

                if ok:
                    return True
    return False


def is_full(b):
    """Kiểm tra bàn đã đầy"""
    return all(cell != " " for cell in b)


def evaluate(b,AI,PLAYER):
    """Hàm lượng giá cho Minimax / Alpha-Beta"""
    if winner(b, AI):      # AI thắng
        return 1
    elif winner(b, PLAYER):    # Người thắng
        return -1
    else:                   # Hòa hoặc chưa kết thúc
        return 0

def heuristic_score(b, AI, PLAYER):
    """
    Heuristic cho bàn N×N:
    + Cộng điểm cho các chuỗi gần thắng của AI
    + Trừ điểm cho chuỗi gần thắng của người chơi
    """
    # Nếu bạn đã có biến BOARD_N, WIN_LENGTH ở đầu file thì dùng lại
    try:
        n = BOARD_N
        k = WIN_LENGTH
    except NameError:
        # fallback cho 3x3
        n = 3
        k = 3

    def idx(r, c):
        return r * n + c

    directions = [
        (1, 0),   # dọc
        (0, 1),   # ngang
        (1, 1),   # chéo xuống phải
        (1, -1),  # chéo xuống trái
    ]

    score = 0

    for r in range(n):
        for c in range(n):
            for dr, dc in directions:
                end_r = r + (k - 1) * dr
                end_c = c + (k - 1) * dc
                if not (0 <= end_r < n and 0 <= end_c < n):
                    continue

                cells = []
                for step in range(k):
                    rr = r + step * dr
                    cc = c + step * dc
                    cells.append(idx(rr, cc))

                line = [b[p] for p in cells]

                # Nếu cả AI và PLAYER cùng có trong đoạn này thì bỏ
                if AI in line and PLAYER in line:
                    continue

                ai_cnt = line.count(AI)
                pl_cnt = line.count(PLAYER)

                if ai_cnt > 0 and pl_cnt == 0:
                    # càng nhiều quân AI trong 1 đoạn k ô càng mạnh
                    score += ai_cnt * ai_cnt * 10
                elif pl_cnt > 0 and ai_cnt == 0:
                    # càng nhiều quân người chơi trong 1 đoạn càng nguy hiểm
                    score -= pl_cnt * pl_cnt * 10

    return score


def print_board(b):
    """In bàn cờ ra console (hỗ trợ debug)"""
    n = BOARD_N
    print("\n")
    for i in range(n):
        row = b[i*n:(i+1)*n]
        print(" " + " | ".join(row))
        if i < n-1:
            print("---+" * (n-1) + "---")
    print("\n")
