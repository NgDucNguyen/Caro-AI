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
