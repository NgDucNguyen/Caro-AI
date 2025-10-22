# --- Các hàm xử lý bàn cờ Tic Tac Toe ---

def winner(b, player):
    """Kiểm tra người thắng"""
    win_states = [
        [0,1,2], [3,4,5], [6,7,8],  # hàng ngang
        [0,3,6], [1,4,7], [2,5,8],  # cột dọc
        [0,4,8], [2,4,6]            # đường chéo
    ]
    for state in win_states:
        if b[state[0]] == b[state[1]] == b[state[2]] == player:
            return True
    return False


def is_full(b):
    """Kiểm tra bàn đã đầy"""
    return " " not in b


def evaluate(b):
    """Hàm lượng giá cho Minimax"""
    if winner(b, "O"):
        return 1
    elif winner(b, "X"):
        return -1
    else:
        return 0
