import pygame, sys, os
import argparse
import subprocess  # Thư viện để chạy biểu đồ riêng biệt

# lấy tham số từ Launcher
parser = argparse.ArgumentParser()
parser.add_argument("--mode")
parser.add_argument("--size")
parser.add_argument("--winlen")
parser.add_argument("--player", default="X")
parser.add_argument("--algo", default="ab")
parser.add_argument("--depth", default="4")

# Nhận cờ hiển thị biểu đồ từ Launcher
parser.add_argument("--show_chart", action="store_true")

args = parser.parse_args()

MODE = args.mode.lower() # pvp or pve

PLAYER = args.player.upper()
AI = "O" if PLAYER == "X" else "X"
DEPTH = int(args.depth)
BOARD_N = int(args.size)
WIN_LEN = int(args.winlen)
SHOW_CHART_ON_END = args.show_chart  # Lưu trạng thái cờ

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend import features

# Khởi tạo bàn cờ N×N cho backend
features.init_board(BOARD_N, WIN_LEN)

# Chon thuat toan AI
algo = args.algo.lower()

if algo == "ab":
    features.ALGORITHM_MODE = "alpha"
    features.set_algorithm(True)
elif algo == "pure":
    features.ALGORITHM_MODE = "minimax"
    features.set_algorithm(False)
else:
    # không dùng minimax, random hoàn toàn
    features.ALGORITHM_MODE = "none"

features.set_search_depth(DEPTH)

# Nếu chơi PVP thi tat AI
if MODE == "pvp":
    features.ALGORITHM_MODE = "none"

features.init_player_symbols(PLAYER, AI)

if PLAYER == "X":
    features.player_turn = True
else:
    features.player_turn = False
pygame.init()

# Window
WINDOW_W, WINDOW_H = 1300, 740
screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
pygame.display.set_caption("Caro AI Project")

# Colors and layout
BG_TOP = (10, 20, 40)
BG_BOTTOM = (5, 10, 25)
WHITE = (255, 255, 255)
BOARD_BG = (255, 249, 230)
X_COLOR = (35, 90, 200)
O_COLOR = (220, 50, 50)
TEXT = (10, 10, 15)
CARD = (255, 255, 255)
BTN_BG = (10, 15, 25)
BTN_BG_HOVER = (40, 50, 70)

# Layout setup
LEFT_PANEL_X = 40
LEFT_PANEL_W = 300
RIGHT_PANEL_X = WINDOW_W - 340
RIGHT_PANEL_W = 300

free_width = RIGHT_PANEL_X - (LEFT_PANEL_X + LEFT_PANEL_W)
TOP_MARGIN = 150
BOTTOM_MARGIN = 40
free_height = WINDOW_H - TOP_MARGIN - BOTTOM_MARGIN
INNER_MARGIN_X = 20
max_board_by_width = free_width - 2 * INNER_MARGIN_X
max_board_pixels = min(max_board_by_width, free_height)
cell_size = max(40, min(150, max_board_pixels // BOARD_N))
board_width = cell_size * BOARD_N
board_height = board_width
board_x = LEFT_PANEL_X + LEFT_PANEL_W + (free_width - board_width) // 2
board_y = TOP_MARGIN + (free_height - board_height) // 2

clock = pygame.time.Clock()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def font(size, weight="regular"):
    # Fallback font hệ thống nếu không có font assets
    return pygame.font.SysFont("arial", size, bold=(weight in ["bold", "semibold"]))

def gradient():
    # Vẽ gradient đơn giản hóa để tối ưu hiệu năng
    screen.fill(BG_TOP)

def draw_board():
    pygame.draw.rect(
        screen,
        BOARD_BG,
        (board_x - 10, board_y - 10, cell_size * BOARD_N + 20, cell_size * BOARD_N + 20),
        border_radius=12
    )
    for i, v in enumerate(features.board):
        r = i // BOARD_N
        c = i % BOARD_N
        x = board_x + c * cell_size
        y = board_y + r * cell_size
        rect = pygame.Rect(x, y, cell_size, cell_size)

        mx, my = pygame.mouse.get_pos()
        if rect.collidepoint((mx, my)) and features.board[i] == " " and not features.game_over:
            pygame.draw.rect(screen, (255, 235, 120), rect)
        elif i in features.highlight_cells:
            pygame.draw.rect(screen, (210, 255, 240), rect)
        else:
            pygame.draw.rect(screen, BOARD_BG, rect)
        pygame.draw.rect(screen, (240, 200, 120), rect, 2) # Giảm độ dày viền ô chút cho thanh thoát

        cx, cy = x + cell_size // 2, y + cell_size // 2
        mark_thickness = max(2, cell_size // 8)
        off = cell_size // 3
        radius = cell_size // 3

        if v == "X":
            pygame.draw.line(screen, X_COLOR, (cx - off, cy - off), (cx + off, cy + off), mark_thickness)
            pygame.draw.line(screen, X_COLOR, (cx + off, cy - off), (cx - off, cy + off), mark_thickness)
        elif v == "O":
            pygame.draw.circle(screen, O_COLOR, (cx, cy), radius, mark_thickness)

def draw_panel():
    # Left Panel
    pygame.draw.rect(screen, CARD, (40, 160, 300, 450), border_radius=18)
    t = font(20, "bold").render("Game Status", True, TEXT)
    screen.blit(t, (60, 180))

    if features.game_over:
        msg = features.winner_text
        col = (20, 180, 60) if "win" in msg else (100, 100, 100)
        g = font(20).render(msg, True, col)
        screen.blit(g, (60, 230))
    else:
        if MODE == "pvp":
            curr = f"Player {'X' if features.player_turn else 'O'}"
        else:
            curr = f"Player {PLAYER}" if features.player_turn else f"Computer ({AI})"
        
        g = font(18, "medium").render(f"Turn: {curr}", True, (60, 60, 60))
        screen.blit(g, (60, 230))

    # Buttons helper
    def btn(x, y, w, h, text, active=True):
        mx, my = pygame.mouse.get_pos()
        rect = pygame.Rect(x, y, w, h)
        if active:
            color = BTN_BG_HOVER if rect.collidepoint((mx, my)) else BTN_BG
        else:
            color = (150, 150, 150)
        
        pygame.draw.rect(screen, color, rect, border_radius=12)
        label = font(18).render(text, True, WHITE)
        screen.blit(label, (x + w // 2 - label.get_width() // 2, y + h // 2 - label.get_height() // 2))

    btn(60, 300, 260, 55, "New Game")
    undo_enabled = (len(features.move_history) > 0) and (not features.game_over) and features.player_turn
    btn(60, 370, 260, 55, "Undo", active=undo_enabled)

    # Right Panel
    pygame.draw.rect(screen, CARD, (WINDOW_W - 340, 160, 300, 450), border_radius=18)
    title = font(22, "semibold").render("Score & Log", True, TEXT)
    screen.blit(title, (WINDOW_W - 320, 180))
    
    st = font(18)
    screen.blit(st.render(f"Player {PLAYER}: {features.scores[PLAYER]}", True, X_COLOR if PLAYER == "X" else O_COLOR), (WINDOW_W - 320, 230))
    screen.blit(st.render(f"Computer ({AI}): {features.scores[AI]}", True, O_COLOR if AI == "O" else X_COLOR), (WINDOW_W - 320, 265))
    screen.blit(st.render(f"Draws: {features.scores['D']}", True, (60, 60, 60)), (WINDOW_W - 320, 300))
    
    # Log AI
    log_y = 350
    screen.blit(st.render("AI Thinking Log:", True, (80, 80, 80)), (WINDOW_W - 320, log_y))
    log_y += 30

    for idx, t_val in enumerate(features.ai_time_log[-7:]): # Lấy 7 dòng cuối
        log_line = st.render(f"Move: {t_val:.4f}s", True, (100, 100, 100))
        screen.blit(log_line, (WINDOW_W - 320, log_y))
        log_y += 25

def tick():
    if MODE == "pvp":
        return
    
    if not features.game_over and not features.player_turn:
        pygame.time.delay(100)
        features.apply_ai_move()


def main():
    has_shown_chart = False # Biến cờ kiểm tra biểu đồ
    while True:
        clock.tick(60)
        gradient()
        title = font(42, "bold").render("CARO AI PROJECT", True, WHITE)
        screen.blit(title, (WINDOW_W // 2 - title.get_width() // 2, 50))
        
        draw_board()
        draw_panel()
        pygame.display.update()

        # LOGIC TỰ ĐỘNG MỞ BIỂU ĐỒ
        if features.game_over and SHOW_CHART_ON_END and not has_shown_chart:
            # Dùng tiếng Anh để không lỗi bảng mã Windows
            print("[INFO] Game Over. Launching chart...") 
            
            # Tìm đường dẫn đến file chart_utils.py
            chart_script = os.path.join(PROJECT_ROOT, "backend", "chart_utils.py")
            
            if os.path.exists(chart_script):
                try:
                    # Mở process riêng để không làm đơ game
                    subprocess.Popen([sys.executable, chart_script])
                except Exception as e:
                    print(f"Chart Error: {e}")
            else:
                print(f"File not found: {chart_script}")
            
            has_shown_chart = True # Đánh dấu đã mở

        # Reset cờ khi chơi ván mới
        if not features.game_over:
            has_shown_chart = False

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                # xoá dữ liệu cũ khi thoát game
                log_path = os.path.join(PROJECT_ROOT, "ai_performance_log.csv")
                if os.path.exists(log_path):
                    try:
                        os.remove(log_path) # Xóa file log ngay lập tức
                        print("[INFO] Đã dọn dẹp dữ liệu log.")
                    except Exception as err:
                        print(f"[Lỗi] Không xóa được log: {err}")
                pygame.quit()
                sys.exit()

            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                x, y = e.pos
                # Xử lý nút bấm
                if 60 <= x <= 320:
                    if 300 <= y <= 355:
                        features.reset_game()
                    if 370 <= y <= 425 and (len(features.move_history) > 0) and (not features.game_over) and features.player_turn:
                        features.undo()

                # Xử lý click bàn cờ
                allow_click = False
                if MODE == "pvp":
                    allow_click = not features.game_over
                else:
                    allow_click = (not features.game_over and features.player_turn)

                if allow_click:
                    for i in range(len(features.board)):
                        r = i // BOARD_N
                        c = i % BOARD_N
                        rect = pygame.Rect(
                            board_x + c * cell_size,
                            board_y + r * cell_size,
                            cell_size,
                            cell_size
                        )
                        if rect.collidepoint((x, y)) and features.board[i] == " ":
                            features.apply_player_move(i)
                            break
        tick()

if __name__=="__main__":
    main()