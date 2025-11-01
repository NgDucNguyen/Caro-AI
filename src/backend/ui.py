"""
import pygame
import sys
from game import winner, is_full
from minimax import best_move

pygame.init()

# --- Cấu hình ---
WIDTH, HEIGHT = 600, 700
CELL_SIZE = WIDTH // 3
BG_COLOR = (245, 245, 245)
LINE_COLOR = (180, 180, 180)
X_COLOR = (240, 100, 100)
O_COLOR = (90, 130, 250)
WIN_HIGHLIGHT = (255, 220, 120)
BTN_COLOR = (230, 230, 230)
BTN_HOVER = (200, 200, 200)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🎮 Tic Tac Toe AI")
FONT = pygame.font.SysFont("poppins", 100, bold=True)
TEXT_FONT = pygame.font.SysFont("poppins", 36, bold=True)
BTN_FONT = pygame.font.SysFont("poppins", 28, bold=True)

# --- Biến ---
board = [" " for _ in range(9)]
game_over = False
winner_text = ""
highlight_cells = []


# --- Vẽ bàn cờ ---
def draw_board():
    screen.fill(BG_COLOR)

    # Vẽ highlight ô thắng (nếu có)
    for i in highlight_cells:
        rect = pygame.Rect((i % 3) * CELL_SIZE, (i // 3) * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, WIN_HIGHLIGHT, rect)

    # Vẽ các đường kẻ
    for i in range(1, 3):
        pygame.draw.line(screen, LINE_COLOR, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), 5)
        pygame.draw.line(screen, LINE_COLOR, (i * CELL_SIZE, 0), (i * CELL_SIZE, WIDTH), 5)

    # Vẽ X và O
    for i, cell in enumerate(board):
        x = (i % 3) * CELL_SIZE + CELL_SIZE // 2
        y = (i // 3) * CELL_SIZE + CELL_SIZE // 2
        if cell == "X":
            text = FONT.render("X", True, X_COLOR)
        elif cell == "O":
            text = FONT.render("O", True, O_COLOR)
        else:
            continue
        screen.blit(text, text.get_rect(center=(x, y)))


# --- Nút bấm ---
def draw_button(text, y, hover):
    color = BTN_HOVER if hover else BTN_COLOR
    rect = pygame.Rect(WIDTH // 2 - 100, y, 200, 60)
    pygame.draw.rect(screen, color, rect, border_radius=15)
    label = BTN_FONT.render(text, True, (30, 30, 30))
    screen.blit(label, label.get_rect(center=rect.center))
    return rect


# --- Xác định click ô ---
def get_cell(pos):
    x, y = pos
    if y > WIDTH:
        return None
    row, col = y // CELL_SIZE, x // CELL_SIZE
    return row * 3 + col


# --- Reset game ---
def reset_game():
    global board, game_over, winner_text, highlight_cells
    board = [" " for _ in range(9)]
    game_over = False
    winner_text = ""
    highlight_cells = []


# --- Highlight 3 ô thắng ---
def get_winning_cells(b, mark):
    wins = [(0,1,2), (3,4,5), (6,7,8),
            (0,3,6), (1,4,7), (2,5,8),
            (0,4,8), (2,4,6)]
    for a,b_,c in wins:
        if b[a] == b[b_] == b[c] == mark:
            return [a,b_,c]
    return []


# --- Hiệu ứng chữ thắng ---
def draw_text_effect(text):
    render = TEXT_FONT.render(text, True, (20, 20, 20))
    screen.blit(render, render.get_rect(center=(WIDTH//2, WIDTH + 50)))


# --- Main loop ---
def main():
    global game_over, winner_text, highlight_cells
    running = True
    player_turn = True

    while running:
        mouse = pygame.mouse.get_pos()
        draw_board()

        # Khi game kết thúc: vẽ thông báo + nút
        if game_over:
            draw_text_effect(winner_text)
            play_rect = draw_button("Chơi lại", 550, False)
            quit_rect = draw_button("Thoát", 620, False)
        else:
            play_rect = quit_rect = None

        pygame.display.flip()

        # --- Sự kiện ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_over:
                    if play_rect and play_rect.collidepoint(event.pos):
                        reset_game()
                    elif quit_rect and quit_rect.collidepoint(event.pos):
                        running = False
                        pygame.quit()
                        sys.exit()
                else:
                    idx = get_cell(event.pos)
                    if idx is not None and board[idx] == " " and player_turn:
                        board[idx] = "X"

                        if winner(board, "X"):
                            highlight_cells = get_winning_cells(board, "X")
                            winner_text = "🎉 Bạn thắng!"
                            game_over = True
                        elif is_full(board):
                            winner_text = "🤝 Hòa!"
                            game_over = True
                        else:
                            player_turn = False

        # --- Máy đánh ---
        if not game_over and not player_turn:
            pygame.time.delay(400)
            move = best_move(board)
            if move is not None:
                board[move] = "O"

            if winner(board, "O"):
                highlight_cells = get_winning_cells(board, "O")
                winner_text = "💻 Máy thắng!"
                game_over = True
            elif is_full(board):
                winner_text = "🤝 Hòa!"
                game_over = True

            player_turn = True


if __name__ == "__main__":
    main()
"""















"""
import pygame, sys, time, random, os
from game import winner, is_full
from minimax import best_move

pygame.init()

# ---------------- Window ----------------
WINDOW_W, WINDOW_H = 1300, 740
screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
pygame.display.set_caption("Caro AI Project")

# ----------- Theme Colors -----------
BG_TOP = (10, 20, 40)
BG_BOTTOM = (5, 10, 25)
WHITE = (255,255,255)
BOARD_BG = (255, 249, 230)
WIN_BG = (255, 245, 200)
HOVER_BG = (210,255,240)
X_COLOR = (35, 90, 200)
O_COLOR = (220,50,50)
TEXT = (10,10,15)
CARD = (255,255,255)
BTN_BG = (10,15,25)
BTN_BG_HOVER = (40,50,70)

# -------- Board settings --------
BOARD_N = 3
WINLEN = 3
board = [" "] * 9
cell_size = 150
board_x = (WINDOW_W//2 - cell_size*BOARD_N//2)
board_y = 180

scores = {"X":0, "O":0, "D":0}
winner_text = ""
game_over = False
move_history = []
highlight_cells = []
player_turn = True

clock = pygame.time.Clock()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def font(size, weight="regular"):
    font_path = os.path.join(BASE_DIR, "../../assets/fonts", f"Poppins-{weight.capitalize()}.ttf")
    font_path = os.path.normpath(font_path)
    return pygame.font.Font(font_path, size)

# Draw Gradient Background
def gradient():
    for i in range(WINDOW_H):
        r = BG_TOP[0] + (BG_BOTTOM[0]-BG_TOP[0])*i/WINDOW_H
        g = BG_TOP[1] + (BG_BOTTOM[1]-BG_TOP[1])*i/WINDOW_H
        b = BG_TOP[2] + (BG_BOTTOM[2]-BG_TOP[2])*i/WINDOW_H
        pygame.draw.line(screen, (int(r),int(g),int(b)), (0,i), (WINDOW_W,i))

def draw_board():
    pygame.draw.rect(screen, BOARD_BG, (board_x-10, board_y-10, cell_size*3+20, cell_size*3+20), border_radius=12)

    for i,v in enumerate(board):
        r = i//3; c = i%3
        x = board_x + c*cell_size
        y = board_y + r*cell_size
        rect = pygame.Rect(x,y,cell_size,cell_size)

        mx, my = pygame.mouse.get_pos()

        # Highlight when mouse over empty cell (hover)
        if rect.collidepoint((mx, my)) and board[i] == " ":
            pygame.draw.rect(screen, (255, 235, 120), rect)  # vàng hover
        # Highlight winning cells
        elif i in highlight_cells:
            pygame.draw.rect(screen, (210,255,240), rect)  # xanh khi thắng
        else:
            pygame.draw.rect(screen, BOARD_BG, rect)  # nền ô vàng

        # Grid line
        pygame.draw.rect(screen, (240,200,120), rect, 4)

        # Draw X / O
        cx,cy = x+cell_size//2, y+cell_size//2
        if v == "X":
            off = 40
            pygame.draw.line(screen, X_COLOR,(cx-off,cy-off),(cx+off,cy+off),10)
            pygame.draw.line(screen, X_COLOR,(cx+off,cy-off),(cx-off,cy+off),10)
        elif v == "O":
            pygame.draw.circle(screen, O_COLOR, (cx,cy), 50, 10)

def draw_panel():
    # Status panel
    pygame.draw.rect(screen, CARD,(40,160,300,450), border_radius=18)
    t = font(20,"bold").render("Game Status",True,TEXT)
    screen.blit(t,(60,180))

    if game_over:
        g = font(20).render(winner_text,True,(20,200,80))
        screen.blit(g,(60,230))
    else:
        cur = "Player X" if player_turn else "Computer"
        g = font(18, "medium").render(f"Turn: {cur}",True,(60,60,60))
        screen.blit(g,(60,230))

    # Buttons
    def btn(x,y,w,h,text,active=True):
        mx,my = pygame.mouse.get_pos()
        color = BTN_BG_HOVER if pygame.Rect(x,y,w,h).collidepoint((mx,my)) else BTN_BG
        pygame.draw.rect(screen,color,(x,y,w,h),border_radius=12)
        label = font(18).render(text,True,WHITE)
        screen.blit(label,(x+w//2 - label.get_width()//2,y+h//2-label.get_height()//2))

    btn(60,300,260,55,"New Game")
    
    undo_enabled = (len(move_history) > 0) and (not game_over) and player_turn
    btn(60,370,260,55,"Undo",active=undo_enabled)

    # Score Panel
    pygame.draw.rect(screen, CARD,(WINDOW_W-340,160,300,450), border_radius=18)
    title = font(22,"semibold").render("Score",True,TEXT)
    screen.blit(title,(WINDOW_W-320,180))

    st = font(18)
    screen.blit(st.render(f"Player X: {scores['X']}",True,X_COLOR),(WINDOW_W-320,230))
    screen.blit(st.render(f"Player O: {scores['O']}",True,O_COLOR),(WINDOW_W-320,265))
    screen.blit(st.render(f"Draws: {scores['D']}",True,(60,60,60)),(WINDOW_W-320,300))

def reset_game():
    global board,move_history,game_over,winner_text,player_turn, highlight_cells
    board=[" "]*9; move_history=[]; game_over=False; winner_text=""; player_turn=True; highlight_cells = []

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

def best_ai_move():
    try: return best_move(board)
    except: return random.choice([i for i,v in enumerate(board) if v==" "])

def tick():
    global player_turn,game_over,winner_text
    
    if not game_over and not player_turn:
        pygame.time.delay(300)
        move = best_ai_move()
        board[move] = "O"
        move_history.append(move)

        if winner(board,"O"):
            highlight_cells[:] = get_winning_cells(board,"O")
            winner_text="Computer wins!"
            game_over=True; scores["O"]+=1
        elif is_full(board):
            winner_text="Draw!"
            game_over=True; scores["D"]+=1
        player_turn=True

def get_winning_cells(b, mark):
    lines = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
    for a,b_,c in lines:
        if b[a]==b[b_]==b[c]==mark:
            return [a,b_,c]
    return []

def main():
    global player_turn, game_over, winner_text
    while True:
        clock.tick(60)
        gradient()

        # Title
        title = font(42,"bold").render("CARO AI PROJECT",True,WHITE)
        screen.blit(title,(WINDOW_W//2-title.get_width()//2,50))

        draw_board()
        draw_panel()

        pygame.display.update()

        for e in pygame.event.get():
            if e.type==pygame.QUIT: pygame.quit();sys.exit()
            if e.type==pygame.MOUSEBUTTONDOWN and e.button==1:
                x,y = e.pos

                # Buttons
                if 60<=x<=320:
                    if 300<=y<=355: reset_game()
                    if 370<=y<=425 and (len(move_history) > 0) and (not game_over) and player_turn: undo()

                # Board click
                if not game_over:
                    for i in range(9):
                        r=i//3;c=i%3
                        rect=pygame.Rect(board_x+c*cell_size,board_y+r*cell_size,cell_size,cell_size)
                        if rect.collidepoint((x,y)) and board[i]==" " and player_turn:
                            board[i]="X"; move_history.append(i)
                            if winner(board,"X"):
                                highlight_cells[:] = get_winning_cells(board, "X")
                                winner_text="You win!"
                                game_over=True; scores["X"]+=1
                            elif is_full(board):
                                winner_text="Draw!"; game_over=True; scores["D"]+=1
                            player_turn=False
        tick()

if __name__=="__main__":
    main()
"""