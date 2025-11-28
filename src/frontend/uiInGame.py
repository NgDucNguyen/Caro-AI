import pygame, sys, os
import argparse

# lấy tham số từ Launcher
parser = argparse.ArgumentParser()
parser.add_argument("--mode")
parser.add_argument("--size")
parser.add_argument("--winlen")
parser.add_argument("--player",default="X")
parser.add_argument("--algo", default="ab")
args = parser.parse_args()

PLAYER = args.player.upper()
AI="O" if PLAYER == "X" else "X"


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend import features

#Chon thuat toan AI
algo = args.algo.lower()
if algo == "ab":
    features.set_algorithm(True)
else:
    features.set_algorithm(False)

features.init_player_symbols(PLAYER,AI)

if PLAYER == "X":
    features.player_turn = True
else:
    features.player_turn = False
pygame.init()

# Window
WINDOW_W, WINDOW_H = 1300, 740
screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
pygame.display.set_caption("Caro AI Project")

# Colors and layout (kept from original)
BG_TOP = (10, 20, 40)
BG_BOTTOM = (5, 10, 25)
WHITE = (255,255,255)
BOARD_BG = (255, 249, 230)
X_COLOR = (35, 90, 200)
O_COLOR = (220,50,50)
TEXT = (10,10,15)
CARD = (255,255,255)
BTN_BG = (10,15,25)
BTN_BG_HOVER = (40,50,70)

# Board settings
BOARD_N = 3
cell_size = 150
board_x = (WINDOW_W//2 - cell_size*BOARD_N//2)
board_y = 180

clock = pygame.time.Clock()

# Base direction -> assets
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
def font(size, weight="regular"):
    font_path = os.path.join(BASE_DIR, "../../assets/fonts", f"Poppins-{weight.capitalize()}.ttf")
    font_path = os.path.normpath(font_path)
    return pygame.font.Font(font_path, size)

def gradient():
    for i in range(WINDOW_H):
        r = BG_TOP[0] + (BG_BOTTOM[0]-BG_TOP[0])*i/WINDOW_H
        g = BG_TOP[1] + (BG_BOTTOM[1]-BG_TOP[1])*i/WINDOW_H
        b = BG_TOP[2] + (BG_BOTTOM[2]-BG_TOP[2])*i/WINDOW_H
        pygame.draw.line(screen, (int(r),int(g),int(b)), (0,i), (WINDOW_W,i))

def draw_board():
    pygame.draw.rect(screen, BOARD_BG, (board_x-10, board_y-10, cell_size*3+20, cell_size*3+20), border_radius=12)
    for i,v in enumerate(features.board):
        r = i//3; c = i%3
        x = board_x + c*cell_size
        y = board_y + r*cell_size
        rect = pygame.Rect(x,y,cell_size,cell_size)

        mx, my = pygame.mouse.get_pos()
        if rect.collidepoint((mx, my)) and features.board[i] == " ":
            pygame.draw.rect(screen, (255, 235, 120), rect)
        elif i in features.highlight_cells:
            pygame.draw.rect(screen, (210,255,240), rect)
        else:
            pygame.draw.rect(screen, BOARD_BG, rect)
        pygame.draw.rect(screen, (240,200,120), rect, 4)

        cx,cy = x+cell_size//2, y+cell_size//2
        if v == "X":
            off = 40
            pygame.draw.line(screen, X_COLOR,(cx-off,cy-off),(cx+off,cy+off),10)
            pygame.draw.line(screen, X_COLOR,(cx+off,cy-off),(cx-off,cy+off),10)
        elif v == "O":
            pygame.draw.circle(screen, O_COLOR, (cx,cy), 50, 10)

def draw_panel():
    pygame.draw.rect(screen, CARD,(40,160,300,450), border_radius=18)
    t = font(20,"bold").render("Game Status",True,TEXT)
    screen.blit(t,(60,180))

    if features.game_over:
        g = font(20).render(features.winner_text,True,(20,200,80))
        screen.blit(g,(60,230))
    else:
        cur = f"Player {PLAYER}" if features.player_turn else f"Computer ({AI})"
        g = font(18, "medium").render(f"Turn: {cur}",True,(60,60,60))
        screen.blit(g,(60,230))

    def btn(x,y,w,h,text,active=True):
        mx,my = pygame.mouse.get_pos()
        color = BTN_BG_HOVER if pygame.Rect(x,y,w,h).collidepoint((mx,my)) else BTN_BG
        pygame.draw.rect(screen,color,(x,y,w,h),border_radius=12)
        label = font(18).render(text,True,WHITE)
        screen.blit(label,(x+w//2 - label.get_width()//2,y+h//2-label.get_height()//2))
    btn(60,300,260,55,"New Game")
    undo_enabled = (len(features.move_history) > 0) and (not features.game_over) and features.player_turn
    btn(60,370,260,55,"Undo",active=undo_enabled)

    pygame.draw.rect(screen, CARD,(WINDOW_W-340,160,300,450), border_radius=18)
    title = font(22,"semibold").render("Score",True,TEXT)
    screen.blit(title,(WINDOW_W-320,180))
    st = font(18)
    screen.blit(st.render(f"Player {PLAYER}: {features.scores[PLAYER]}",True,X_COLOR if PLAYER=="X" else O_COLOR),(WINDOW_W-320,230))
    screen.blit(st.render(f"Computer ({AI}): {features.scores[AI]}",True,O_COLOR if AI=="O" else X_COLOR),(WINDOW_W-320,265))
    screen.blit(st.render(f"Draws: {features.scores['D']}",True,(60,60,60)),(WINDOW_W-320,300))
    
    tt = st.render(f"AI time: {features.ai_total_time:.4f}s", True, (120, 120, 120))
    screen.blit(tt, (WINDOW_W - 320, 335))
    
    # LOG nhiều lần đánh của AI
    log_y = 370
    screen.blit(st.render("AI Thinking Log:", True, (80,80,80)), (WINDOW_W - 320, log_y))
    log_y += 30

    for idx, t in enumerate(features.ai_time_log[-8:]):
        log_line = st.render(f"{idx+1}. {t:.4f}s", True, (100,100,100))
        screen.blit(log_line, (WINDOW_W - 320, log_y))
        log_y += 25

def tick():
    # call engine to perform AI move if needed
    if not features.game_over and not features.player_turn:
        pygame.time.delay(300)
        features.apply_ai_move()

def main():
    while True:
        clock.tick(60)
        gradient()
        title = font(42,"bold").render("CARO AI PROJECT",True,WHITE)
        screen.blit(title,(WINDOW_W//2-title.get_width()//2,50))
        draw_board()
        draw_panel()
        pygame.display.update()

        for e in pygame.event.get():
            if e.type==pygame.QUIT: pygame.quit(); sys.exit()
            if e.type==pygame.MOUSEBUTTONDOWN and e.button==1:
                x,y = e.pos
                # Buttons
                if 60<=x<=320:
                    if 300<=y<=355: features.reset_game()
                    if 370<=y<=425 and (len(features.move_history) > 0) and (not features.game_over) and features.player_turn: features.undo()
                # Board click
                if not features.game_over and features.player_turn:
                    for i in range(9):
                        r=i//3;c=i%3
                        rect=pygame.Rect(board_x+c*cell_size,board_y+r*cell_size,cell_size,cell_size)
                        if rect.collidepoint((x,y)) and features.board[i]==" ":
                            features.apply_player_move(i)
        tick()

if __name__=="__main__":
    main()
