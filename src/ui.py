# src/ui.py

import pygame
import sys
import tkinter as tk # Import thư viện Tkinter
from tkinter import messagebox # Import hàm messagebox
from game import GameLogic 

#cai dat kich huoc man hinh
WIDTH, HEIGHT = 700,700
LINE_WIDTH = 15
SQUARE_SIZE = WIDTH//3

#mau sac
BG_COLOR = (28,170,156)
LINE_COLOR = (23, 145, 135) # Màu đường kẻ
X_COLOR = (84, 84, 84)      # Màu X (Xám đậm)
O_COLOR = (242, 235, 211)   # Màu O (Kem nhạt)

class UI:
    def __init__(self, gameLogic):
        self.game = gameLogic
        
        #khoi tao pygame
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT)) # Tạo cửa sổ game
        pygame.display.set_caption("Tic-Tac-Toe AI Project")     # Đặt tiêu đề cửa sổ
        self.screen.fill(BG_COLOR)                               # Đổ màu nền
        self.font = pygame.font.SysFont("monospace", 70)         # Thiết lập font chữ cho thông báo
        self._draw_lines()
    
    def _draw_lines(self):
        """Vẽ 4 đường kẻ tạo lưới 3x3."""
        # Đường ngang 1 (y=1/3 chiều cao)
        pygame.draw.line(self.screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
        # Đường ngang 2 (y=2/3 chiều cao)
        pygame.draw.line(self.screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
        # Đường dọc 1 (x=1/3 chiều rộng)
        pygame.draw.line(self.screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
        # Đường dọc 2 (x=2/3 chiều rộng)
        pygame.draw.line(self.screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH)
        
    def _draw_figures(self):
        """Vẽ ký hiệu X hoặc O dựa trên dữ liệu từ GameLogic."""
        for row in range(3):
            for col in range(3):
                # Tính tọa độ trung tâm của ô (row, col)
                center_x = col * SQUARE_SIZE + SQUARE_SIZE // 2
                center_y = row * SQUARE_SIZE + SQUARE_SIZE // 2
                
                if self.game.board[row][col] == 'X':
                    offset = SQUARE_SIZE // 4 # Khoảng cách từ tâm ra góc
                    # Vẽ đường chéo 1
                    pygame.draw.line(self.screen, X_COLOR, (center_x - offset, center_y - offset), (center_x + offset, center_y + offset), 15)
                    # Vẽ đường chéo 2
                    pygame.draw.line(self.screen, X_COLOR, (center_x + offset, center_y - offset), (center_x - offset, center_y + offset), 15)
                elif self.game.board[row][col] == 'O':
                    radius = SQUARE_SIZE // 3 # Bán kính hình tròn
                    # Vẽ hình tròn 'O'
                    pygame.draw.circle(self.screen, O_COLOR, (center_x, center_y), radius, 15)
                    
    def _show_result_popup(self):
        """Hien thi hop thoai thong bao ket qua game bang Tkinter."""
        result = self.game.winner

        if result == 'X':
            title = "KET QUA"
            message = "Nguoi choi X THANG! Nhan R de choi lai."
        elif result == 'O':
            title = "KET QUA"
            message = "Nguoi choi O THANG! Nhan R de choi lai."
        elif result == "Draw":
            title = "KET QUA"
            message = "HOA! Khong ai thang. Nhan R de choi lai."
        else:
            return # Khong hien thi neu chua co ket qua

        # Hien thi hop thoai thong bao
        messagebox.showinfo(title, message)
        
    def run_game(self):
        """Vòng lặp chính của Giao diện, quản lý sự kiện."""
        running = True
        
        while running:
            for event in pygame.event.get():
                
                # 1. Xử lý đóng cửa sổ (nhấn nút X)
                if event.type == pygame.QUIT:
                    running = False
                    self.root.destroy() # Đảm bảo đóng cả cửa sổ Tkinter
                    pygame.quit()
                    sys.exit()
                    
                # 2. Xử lý click chuột (chỉ khi game chưa kết thúc)
                if event.type == pygame.MOUSEBUTTONDOWN and not self.game.game_over:
                    if event.button == 1: # Click chuột trái
                        
                        pos_x, pos_y = event.pos # Lấy tọa độ pixel của chuột
                        
                        # Chuyển tọa độ pixel sang tọa độ ma trận (0, 1, 2)
                        clicked_col = pos_x // SQUARE_SIZE
                        clicked_row = pos_y // SQUARE_SIZE
                        
                        # Gọi hàm logic game để thực hiện nước đi
                        self.game.make_move(clicked_row, clicked_col) 
                        
                        if self.game.game_over:
                            self._show_result_popup()

                # 3. Xử lý nhấn phím R để chơi lại
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.game.reset_game()     # Reset logic
                        self.screen.fill(BG_COLOR) # Xóa màn hình
                        self._draw_lines()         # Vẽ lại lưới


            # --- Cập nhật màn hình ---
            self._draw_figures() # Vẽ lại các ký hiệu X/O
            
            # Cập nhật toàn bộ màn hình
            pygame.display.update()
            
    # --- CHẠY GAME ---
if __name__ == '__main__':
    # Tạo đối tượng Logic
    game_logic = GameLogic()
    
    # Tạo đối tượng UI, truyền Logic vào
    game_ui = UI(game_logic)
    try:
        # Bắt đầu vòng lặp giao diện
        game_ui.run_game()
    except Exception as e:
        print(f"\nĐã xảy ra lỗi: {e}")
        print("Đảm bảo bạn đã cài đặt 'numpy' và 'pygame'.")
    