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
    n = BOARD_N
    k = WIN_LENGTH

    def idx(r, c):
        return r * n + c

    directions = [(1,0),(0,1),(1,1),(1,-1)]

    score = 0

    for r in range(n):
        for c in range(n):
            for dr, dc in directions:
                cells = []
                for t in range(k):
                    rr = r + t*dr
                    cc = c + t*dc
                    if not (0 <= rr < n and 0 <= cc < n):
                        break
                    cells.append(idx(rr,cc))
                if len(cells) < k:
                    continue

                line = [b[p] for p in cells]

                if AI in line and PLAYER in line:
                    continue

                ai_cnt = line.count(AI)
                pl_cnt = line.count(PLAYER)

                # kiểm tra độ mở 2 đầu
                left_block = True
                right_block = True

                lr = r - dr
                lc = c - dc
                if 0 <= lr < n and 0 <= lc < n:
                    left_block = (b[idx(lr,lc)] != " ")

                rr = r + k*dr
                rc = c + k*dc
                if 0 <= rr < n and 0 <= rc < n:
                    right_block = (b[idx(rr,rc)] != " ")

                open_ends = 2 - int(left_block) - int(right_block)

                if ai_cnt > 0 and pl_cnt == 0:
                    if ai_cnt == k:
                        return 10_000_000
                    score += (10 ** ai_cnt) * open_ends

                elif pl_cnt > 0 and ai_cnt == 0:
                    if pl_cnt == k:
                        return -10_000_000
                    score -= (10 ** pl_cnt) * open_ends

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
