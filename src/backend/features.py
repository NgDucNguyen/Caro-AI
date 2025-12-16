import pygame, sys, time, random, os
from backend.game import winner, is_full
from backend.minimax import best_move
import backend.minimax as minimax_engine

# Game state
BOARD_N = 3
WIN_LENGTH = 3

board = [" "] * (BOARD_N * BOARD_N)
move_history = []
scores = {"X": 0, "O": 0, "D": 0}
player_turn = True
game_over = False
winner_text = ""
highlight_cells = []

ALGORITHM_MODE = "alpha"   # alpha, minimax, none

#bien thoi gian
ai_last_think_time = 0.0
ai_time_log = []
ai_total_time = 0.0

#Ký hiệu người chơi Ai mặc định
PLAYER = "X"
AI = "O"


def get_current_mark():
    return PLAYER if player_turn else AI

# Khởi tạo kí hiệu
def init_player_symbols(player_symbol, ai_symbol):
    global PLAYER, AI
    PLAYER = player_symbol
    AI = ai_symbol

def init_board(size,winlen):
    """
    Khởi tạo lại bàn cờ N×N và cấu hình cho module game.
    Được gọi từ uiInGame.py sau khi đọc tham số từ launcher.
    """
    global board, move_history, game_over, winner_text, highlight_cells
    global BOARD_N, WIN_LENGTH, player_turn

    BOARD_N = size
    WIN_LENGTH = winlen

    board = [" "] * (BOARD_N * BOARD_N)
    move_history = []
    game_over = False
    winner_text = ""
    highlight_cells = []
    player_turn = True

    # Cập nhật cho game.py
    import backend.game as game_module
    game_module.set_board_params(BOARD_N, WIN_LENGTH)

def reset_game():
    global board, move_history, game_over, winner_text, player_turn, highlight_cells
    global ai_time_log,ai_total_time
    ai_time_log = []
    ai_total_time = 0.0
    
    board = [" "] * (BOARD_N * BOARD_N)
    move_history = []
    game_over = False
    winner_text = ""
    highlight_cells = []
    
    player_turn = (PLAYER=="X")

def undo():
    global player_turn, highlight_cells
    if move_history:
        highlight_cells = []
        p = move_history.pop()
        board[p] = " "
        if move_history:
            a = move_history.pop()
            board[a] = " "
        player_turn = True

def get_winning_cells(b, mark):
    """
    Trả về danh sách index các ô tạo thành chuỗi WIN_LENGTH thắng.
    Nếu không có, trả về [].
    """
    n = BOARD_N
    k = WIN_LENGTH

    def idx(r, c):
        return r * n + c

    directions = [
        (1, 0),
        (0, 1),
        (1, 1),
        (1, -1),
    ]

    for r in range(n):
        for c in range(n):
            if b[idx(r, c)] != mark:
                continue

            for dr, dc in directions:
                end_r = r + (k - 1) * dr
                end_c = c + (k - 1) * dc
                if not (0 <= end_r < n and 0 <= end_c < n):
                    continue

                cells = []
                ok = True
                for step in range(k):
                    rr = r + step * dr
                    cc = c + step * dc
                    if b[idx(rr, cc)] != mark:
                        ok = False
                        break
                    cells.append(idx(rr, cc))

                if ok:
                    return cells
    return []


def apply_player_move(i):
    """Attempt to place X at i. Returns True if move accepted."""
    global player_turn, game_over, winner_text
    if game_over or board[i] != " ":
        return False
    
    # X hoac O tuy luot
    mark = get_current_mark()
    board[i] = mark
    move_history.append(i)

    if winner(board, mark):
        highlight_cells[:] = get_winning_cells(board, mark)
        winner_text = f"({mark}) win!"
        game_over = True
        scores[mark] += 1
    elif is_full(board):
        winner_text = "Draw!"
        game_over = True
        scores["D"] += 1
    else:
        player_turn = not player_turn
    return True

def apply_ai_move():
    """Make AI move (O). Returns move index or None."""
    global player_turn, game_over, winner_text
    global ai_time_log,ai_last_think_time,ai_total_time
    global ALGORITHM_MODE
    if game_over or player_turn:
        return None
    try:
        start = time.time()
        if ALGORITHM_MODE == "none":
           # Đánh random
           empties = [i for i, v in enumerate(board) if v == " "]
           move = random.choice(empties) if empties else None

        else:
           # Minimax hoặc Alpha-Beta
           move = best_move(board, AI, PLAYER)

        ai_last_think_time = time.time() - start
        ai_time_log.append(ai_last_think_time)
        ai_total_time += ai_last_think_time
        print(f"[AI] Thinking time: {ai_last_think_time:.5f}s")
    except Exception:
        empties = [i for i,v in enumerate(board) if v == " "]
        move = random.choice(empties) if empties else None

    if move is None:
        return None

    board[move] = AI
    move_history.append(move)

    if winner(board, AI):
        highlight_cells[:] = get_winning_cells(board, AI)
        winner_text = f"Computer ({AI}) wins!"
        game_over = True
        scores[AI] += 1
    elif is_full(board):
        winner_text = "Draw!"
        game_over = True
        scores["D"] += 1

    player_turn = True
    return move

def set_algorithm(use_ab: bool):
    minimax_engine.USE_ALPHABETA = use_ab
    
def set_search_depth(depth: int):
    """
    Đặt độ sâu tối đa cho minimax (None hoặc số dương).
    """
    if depth is not None and depth > 0:
        minimax_engine.MAX_DEPTH = depth
    else:
        minimax_engine.MAX_DEPTH = None
