# --- Các hàm xử lý bàn cờ Tic Tac Toe ---

def winner(b, player):
    """Kiểm tra người thắng"""
    win_states = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # hàng ngang
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # cột dọc
        [0, 4, 8], [2, 4, 6]              # đường chéo
    ]
    for state in win_states:
        # kiểm tra 3 ô cùng là ký hiệu của player và không trống
        if b[state[0]] == b[state[1]] == b[state[2]] == player and b[state[0]] != " ":
            return True
    return False


def is_full(b):
    """Kiểm tra bàn đã đầy"""
    return all(cell != " " for cell in b)


def evaluate(b):
    """Hàm lượng giá cho Minimax / Alpha-Beta"""
    if winner(b, "O"):      # AI thắng
        return 1
    elif winner(b, "X"):    # Người thắng
        return -1
    else:                   # Hòa hoặc chưa kết thúc
        return 0


def print_board(b):
    """In bàn cờ ra console (hỗ trợ debug)"""
    print("\n")
    for i in range(3):
        print(" " + " | ".join(b[i*3:(i+1)*3]))
        if i < 2:
            print("---+---+---")
    print("\n")
