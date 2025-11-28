import pygame, sys, time, random, os
from backend.game import winner, is_full
from backend.minimax import best_move
import backend.minimax as minimax_engine

# Game state
board = [" "] * 9
move_history = []
scores = {"X": 0, "O": 0, "D": 0}
player_turn = True
game_over = False
winner_text = ""
highlight_cells = []

#bien thoi gian
ai_last_think_time = 0.0
ai_time_log = []
ai_total_time = 0.0

#Ký hiệu người chơi Ai mặc định
PLAYER = "X"
AI = "O"

# Khởi tạo kí hiệu
def init_player_symbols(player_symbol, ai_symbol):
    global PLAYER, AI
    PLAYER = player_symbol
    AI = ai_symbol



def reset_game():
    global board, move_history, game_over, winner_text, player_turn, highlight_cells
    global ai_time_log,ai_total_time
    ai_time_log = []
    ai_total_time = 0.0
    
    board = [" "] * 9
    move_history = []
    game_over = False
    winner_text = ""
    highlight_cells = []
    
    if PLAYER == "X":
        player_turn = True
    else:
        player_turn = False

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
    lines = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
    for a,b_,c in lines:
        if b[a] == b[b_] == b[c] == mark:
            return [a,b_,c]
    return []

def apply_player_move(i):
    """Attempt to place X at i. Returns True if move accepted."""
    global player_turn, game_over, winner_text
    if game_over or board[i] != " ":
        return False
    board[i] = PLAYER
    move_history.append(i)

    if winner(board, PLAYER):
        highlight_cells[:] = get_winning_cells(board, PLAYER)
        winner_text = f"You ({PLAYER}) win!"
        game_over = True
        scores[PLAYER] += 1
    elif is_full(board):
        winner_text = "Draw!"
        game_over = True
        scores["D"] += 1
    else:
        player_turn = False
    return True

def apply_ai_move():
    """Make AI move (O). Returns move index or None."""
    global player_turn, game_over, winner_text,ai_last_think_time,ai_total_time
    
    if game_over or player_turn:
        return None
    try:
        start = time.time()
        move = best_move(board,AI,PLAYER)
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