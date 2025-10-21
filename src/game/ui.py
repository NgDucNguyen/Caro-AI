# ui_canvas_ttt_color.py
# Tic-Tac-Toe GUI dạng Canvas, chọn X/O trước khi chơi + tùy chọn màu X/O.
# Máy dùng heuristic (không minimax): win -> block -> center -> corner -> edge.

import tkinter as tk
from tkinter import ttk, messagebox, colorchooser
from typing import Optional, List, Tuple
import random

Coord = Tuple[int, int]
GRID_SIZE = 3
CELL = 120
PADDING = 20
LINE_W = 4
MARK_W = 10
W = H = PADDING*2 + CELL*GRID_SIZE

LINES = [
    [(0,0),(0,1),(0,2)], [(1,0),(1,1),(1,2)], [(2,0),(2,1),(2,2)],
    [(0,0),(1,0),(2,0)], [(0,1),(1,1),(2,1)], [(0,2),(1,2),(2,2)],
    [(0,0),(1,1),(2,2)], [(0,2),(1,1),(2,0)]
]

class Game:
    def __init__(self):
        self.board: List[List[Optional[str]]] = [[None]*GRID_SIZE for _ in range(GRID_SIZE)]

    def reset(self):
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                self.board[r][c] = None

    def moves(self) -> List[Coord]:
        return [(r,c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if self.board[r][c] is None]

    def make(self, rc: Coord, mark: str) -> bool:
        r,c = rc
        if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE and self.board[r][c] is None and mark in ('X','O'):
            self.board[r][c] = mark
            return True
        return False

    def winner(self) -> Optional[str]:
        for line in LINES:
            a,b,c = line
            va = self.board[a[0]][a[1]]
            vb = self.board[b[0]][b[1]]
            vc = self.board[c[0]][c[1]]
            if va and va == vb == vc:
                return va
        return None

    def winning_line(self) -> Optional[List[Coord]]:
        for line in LINES:
            a,b,c = line
            va = self.board[a[0]][a[1]]
            vb = self.board[b[0]][b[1]]
            vc = self.board[c[0]][c[1]]
            if va and va == vb == vc:
                return line
        return None

    def draw(self) -> bool:
        return self.winner() is None and all(self.board[r][c] is not None
                                             for r in range(GRID_SIZE) for c in range(GRID_SIZE))

    def over(self) -> bool:
        return self.winner() is not None or self.draw()

# ------- AI đơn giản (không minimax) -------
def ai_move(g: Game, ai: str, human: str) -> Coord:
    # 1) Ăn ngay nếu có
    for r,c in g.moves():
        g.board[r][c] = ai
        if g.winner() == ai:
            g.board[r][c] = None
            return (r,c)
        g.board[r][c] = None
    # 2) Chặn đối thủ
    for r,c in g.moves():
        g.board[r][c] = human
        if g.winner() == human:
            g.board[r][c] = None
            return (r,c)
        g.board[r][c] = None
    # 3) Center
    if g.board[1][1] is None:
        return (1,1)
    # 4) Góc
    for rc in [(0,0),(0,2),(2,0),(2,2)]:
        if g.board[rc[0]][rc[1]] is None:
            return rc
    # 5) Cạnh
    for rc in [(0,1),(1,0),(1,2),(2,1)]:
        if g.board[rc[0]][rc[1]] is None:
            return rc
    return random.choice(g.moves())

class TicTacToeCanvasUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Tic-Tac-Toe (Canvas + Màu + Chọn X/O trước)")
        self.game = Game()

        # Trạng thái & cấu hình
        self.player_mark = tk.StringVar(value='X')
        self.ai_mark = tk.StringVar(value='O')
        self.color_x = tk.StringVar(value="#1f6feb")  # xanh dương
        self.color_o = tk.StringVar(value="#e11d48")  # đỏ hồng
        self.grid_color = "#111"                      # màu lưới
        self.win_color = "#2ecc71"                    # màu gạch thắng
        self.started = False                          # phải nhấn Bắt đầu mới chơi

        self._build_controls()
        self._build_canvas()
        self._draw_grid()
        self._update_status()

    # ---------- UI ----------
    def _build_controls(self):
        top = ttk.Frame(self.root, padding=10)
        top.pack(side=tk.TOP, fill=tk.X)

        ttk.Label(top, text="Bạn là:").pack(side=tk.LEFT)
        self.side_cb = ttk.Combobox(top, width=4, state="readonly",
                                    values=['X','O'], textvariable=self.player_mark)
        self.side_cb.pack(side=tk.LEFT, padx=(4,10))
        self.side_cb.bind("<<ComboboxSelected>>", self._on_side_change)

        ttk.Button(top, text="Màu X", command=self._pick_color_x).pack(side=tk.LEFT, padx=2)
        ttk.Button(top, text="Màu O", command=self._pick_color_o).pack(side=tk.LEFT, padx=2)

        ttk.Button(top, text="Bắt đầu", command=self._start_game).pack(side=tk.LEFT, padx=8)
        ttk.Button(top, text="Ván mới", command=self._reset).pack(side=tk.LEFT, padx=2)

        self.status = ttk.Label(self.root, text="", padding=6)
        self.status.pack(fill=tk.X)

    def _build_canvas(self):
        self.canvas = tk.Canvas(self.root, width=W, height=H, bg="white", highlightthickness=0)
        self.canvas.pack(padx=10, pady=10)
        self.canvas.bind("<Button-1>", self._on_click)

    # ---------- Drawing ----------
    def _draw_grid(self):
        self.canvas.delete("all")
        x0 = y0 = PADDING
        x1 = y1 = PADDING + CELL*GRID_SIZE

        # vẽ đường lưới
        for i in range(1, GRID_SIZE):
            x = PADDING + i*CELL
            self.canvas.create_line(x, y0, x, y1, width=LINE_W, fill=self.grid_color)
        for i in range(1, GRID_SIZE):
            y = PADDING + i*CELL
            self.canvas.create_line(x0, y, x1, y, width=LINE_W, fill=self.grid_color)
        self.canvas.create_rectangle(x0, y0, x1, y1, width=LINE_W, outline=self.grid_color)

        # marks
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                v = self.game.board[r][c]
                if v:
                    self._draw_mark(r, c, v)

    def _cell_rect(self, r: int, c: int):
        x = PADDING + c*CELL
        y = PADDING + r*CELL
        return x, y, x+CELL, y+CELL

    def _draw_mark(self, r: int, c: int, mark: str):
        x0, y0, x1, y1 = self._cell_rect(r, c)
        pad = CELL*0.2
        col = self.color_x.get() if mark == 'X' else self.color_o.get()
        if mark == 'X':
            self.canvas.create_line(x0+pad, y0+pad, x1-pad, y1-pad, width=MARK_W, fill=col)
            self.canvas.create_line(x0+pad, y1-pad, x1-pad, y0+pad, width=MARK_W, fill=col)
        else:
            cx = (x0 + x1)/2
            cy = (y0 + y1)/2
            r0 = (CELL/2) - pad
            self.canvas.create_oval(cx-r0, cy-r0, cx+r0, cy+r0, width=MARK_W, outline=col)

    def _highlight_win(self):
        line = self.game.winning_line()
        if not line:
            return
        (r1,c1), (r2,c2) = line[0], line[2]
        x0a, y0a, x1a, y1a = self._cell_rect(r1, c1)
        x0b, y0b, x1b, y1b = self._cell_rect(r2, c2)
        ax = (x0a + x1a) / 2
        ay = (y0a + y1a) / 2
        bx = (x0b + x1b) / 2
        by = (y0b + y1b) / 2
        self.canvas.create_line(ax, ay, bx, by, width=MARK_W, fill=self.win_color)

    # ---------- Interaction ----------
    def _on_click(self, ev):
        # Chưa nhấn Bắt đầu thì chưa cho chơi
        if not self.started:
            messagebox.showinfo("Thông báo", "Hãy chọn X/O rồi nhấn 'Bắt đầu' nhé!")
            return
        if self.game.over():
            return
        cell = self._canvas_to_cell(ev.x, ev.y)
        if cell is None:
            return
        r, c = cell
        if self.game.board[r][c] is not None:
            return
        me = self.player_mark.get()
        self.game.make((r,c), me)
        self._draw_grid()

        if self._check_end(last_mark=me):
            return

        self.status.config(text="Máy đang nghĩ...")
        self.root.after(200, self._ai_turn)

    def _canvas_to_cell(self, x: int, y: int) -> Optional[Coord]:
        if not (PADDING <= x <= PADDING + CELL*GRID_SIZE and PADDING <= y <= PADDING + CELL*GRID_SIZE):
            return None
        c = int((x - PADDING) // CELL)
        r = int((y - PADDING) // CELL)
        return (r, c)

    def _ai_turn(self):
        if self.game.over():
            return
        ai = self.ai_mark.get()
        human = self.player_mark.get()
        r,c = ai_move(self.game, ai, human)
        self.game.make((r,c), ai)
        self._draw_grid()
        self._check_end(last_mark=ai)

    def _check_end(self, last_mark: str) -> bool:
        win = self.game.winner()
        if win is not None:
            who = "Bạn" if win == self.player_mark.get() else "Máy"
            self._highlight_win()
            self.status.config(text=f"{who} thắng!")
            messagebox.showinfo("Kết thúc", f"{who} thắng!")
            return True
        if self.game.draw():
            self.status.config(text="Hòa!")
            messagebox.showinfo("Kết thúc", "Hòa!")
            return True
        # cập nhật lượt
        if last_mark == self.player_mark.get():
            self.status.config(text="Lượt của máy")
        else:
            self.status.config(text="Lượt của bạn")
        return False

    # ---------- Controls logic ----------
    def _on_side_change(self, _evt=None):
        # Chỉ cập nhật nhãn; ai_mark sẽ set khi bắt đầu
        pass

    def _start_game(self):
        # Khóa chọn bên, set AI mark ngược lại, bắt đầu ván
        if self.started:
            return
        pm = self.player_mark.get()
        self.ai_mark.set('O' if pm == 'X' else 'X')
        self.side_cb.configure(state='disabled')
        self.started = True
        self.game.reset()
        self._draw_grid()
        self._update_status()

        # Nếu người chọn O thì AI đi trước
        if pm == 'O':
            self.status.config(text="Máy đang nghĩ...")
            self.root.after(200, self._ai_turn)

    def _reset(self):
        # Cho phép chọn lại bên và bắt đầu lại
        self.started = False
        self.side_cb.configure(state='readonly')
        self.game.reset()
        self._draw_grid()
        self._update_status()

    def _update_status(self):
        if not self.started:
            self.status.config(text="Chọn X/O và nhấn 'Bắt đầu'")
        else:
            self.status.config(text="Lượt của bạn" if self.player_mark.get() == 'X' else "Máy đang nghĩ..." if not self.game.moves() else "Lượt của bạn")

    def _pick_color_x(self):
        c, _ = colorchooser.askcolor(color=self.color_x.get(), title="Chọn màu cho X")
        if c:
            # chuyển (r,g,b) -> '#rrggbb'
            self.color_x.set('#%02x%02x%02x' % (int(c[0]), int(c[1]), int(c[2])))
            self._draw_grid()

    def _pick_color_o(self):
        c, _ = colorchooser.askcolor(color=self.color_o.get(), title="Chọn màu cho O")
        if c:
            self.color_o.set('#%02x%02x%02x' % (int(c[0]), int(c[1]), int(c[2])))
            self._draw_grid()

def main():
    root = tk.Tk()
    app = TicTacToeCanvasUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
