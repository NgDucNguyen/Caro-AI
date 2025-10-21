# tictac_cli_a1.py
# Tic-Tac-Toe console: nhập tọa độ A1..C3 (không dùng minimax)
# - Bạn chọn X/O
# - Máy chơi theo "heuristic" đơn giản: ăn ngay nếu có, chặn nếu cần, rồi ưu tiên center -> góc -> cạnh
# Chạy: python tictac_cli_a1.py

from typing import List, Optional, Tuple
import sys
import random
import re

Coord = Tuple[int, int]  # (row 0..2, col 0..2)

ROWS = ['A','B','C']
COLS = ['1','2','3']

def all_lines():
    # 8 line thắng
    return [
        [(0,0),(0,1),(0,2)], [(1,0),(1,1),(1,2)], [(2,0),(2,1),(2,2)],
        [(0,0),(1,0),(2,0)], [(0,1),(1,1),(2,1)], [(0,2),(1,2),(2,2)],
        [(0,0),(1,1),(2,2)], [(0,2),(1,1),(2,0)]
    ]

LINES = all_lines()

class Game:
    def __init__(self):
        self.board: List[List[Optional[str]]] = [[None]*3 for _ in range(3)]

    def reset(self):
        for r in range(3):
            for c in range(3):
                self.board[r][c] = None

    def copy(self) -> "Game":
        g = Game()
        for r in range(3):
            for c in range(3):
                g.board[r][c] = self.board[r][c]
        return g

    def moves(self) -> List[Coord]:
        return [(r,c) for r in range(3) for c in range(3) if self.board[r][c] is None]

    def make(self, rc: Coord, mark: str) -> bool:
        r,c = rc
        if 0 <= r < 3 and 0 <= c < 3 and self.board[r][c] is None and mark in ('X','O'):
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

    def draw(self) -> bool:
        return self.winner() is None and all(self.board[r][c] is not None for r in range(3) for c in range(3))

    def over(self) -> bool:
        return self.winner() is not None or self.draw()

def print_board(g: Game):
    # Lưới trắng với nhãn A..C / 1..3, ô trống hiển thị dấu chấm •
    header = "    " + "   ".join(COLS)
    sep    = "  +" + "---+"*3
    print(header)
    print(sep)
    for r in range(3):
        row_cells = []
        for c in range(3):
            v = g.board[r][c]
            row_cells.append(v if v is not None else '•')
        print(f"{ROWS[r]} | " + " | ".join(row_cells) + " |")
        print(sep)

def parse_coord(s: str) -> Optional[Coord]:
    """
    Chấp nhận: A1, a1, 1A, 1a, B3, 3b ... (bỏ khoảng trắng).
    Trả về (row, col) hoặc None nếu sai.
    """
    s = s.strip().upper().replace(" ", "")
    if not s:
        return None
    # Mẫu có thể là [A-C][1-3] hoặc [1-3][A-C]
    m = re.fullmatch(r'([ABC])([123])', s)
    if m:
        r = ROWS.index(m.group(1))
        c = COLS.index(m.group(2))
        return (r,c)
    m = re.fullmatch(r'([123])([ABC])', s)
    if m:
        r = ROWS.index(m.group(2))
        c = COLS.index(m.group(1))
        return (r,c)
    return None

def input_coord(prompt: str, g: Game) -> Coord:
    while True:
        raw = input(prompt)
        if raw.lower() in ("q","quit","exit"):
            print("Tạm biệt!")
            sys.exit(0)
        rc = parse_coord(raw)
        if rc is None:
            print("⛔ Định dạng sai. Hãy nhập như A1, b2, 3c ...")
            continue
        if g.board[rc[0]][rc[1]] is not None:
            print("⛔ Ô đã được đánh. Chọn ô khác.")
            continue
        return rc

# ------- AI đơn giản (không minimax) -------
def ai_move(g: Game, ai: str, human: str) -> Coord:
    # 1) Ăn ngay nếu có
    for r,c in g.moves():
        g.board[r][c] = ai
        if g.winner() == ai:
            g.board[r][c] = None
            return (r,c)
        g.board[r][c] = None
    # 2) Chặn đối thủ nếu họ sắp thắng
    for r,c in g.moves():
        g.board[r][c] = human
        if g.winner() == human:
            g.board[r][c] = None
            return (r,c)
        g.board[r][c] = None
    # 3) Trung tâm
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
    # fallback
    return random.choice(g.moves())

def ask_choice(prompt: str, options):
    while True:
        s = input(prompt).strip().upper()
        if s.lower() in ("q","quit","exit"):
            print("Tạm biệt!")
            sys.exit(0)
        if s in options:
            return s
        print(f"Chỉ chọn một trong {sorted(options)}.")

def main():
    print("=== Tic-Tac-Toe (tọa độ A1..C3) ===")
    print("Nhập 'q' để thoát bất kỳ lúc nào.\n")

    human = ask_choice("Bạn chọn X hay O? [X/O] ", {"X","O"})
    ai = "O" if human == "X" else "X"

    g = Game()

    # Máy đi trước nếu bạn là O
    if human == "O":
        r,c = ai_move(g, ai, human)
        g.make((r,c), ai)

    while True:
        print_board(g)
        if g.over():
            break

        # Lượt người
        rc = input_coord("Chọn ô (A1..C3 hoặc 1A..3C): ", g)
        g.make(rc, human)

        if g.over():
            print_board(g)
            break

        # Lượt máy
        rc_ai = ai_move(g, ai, human)
        g.make(rc_ai, ai)

    w = g.winner()
    if w is None:
        print("Hòa!")
    elif w == human:
        print("Bạn thắng! 🎉")
    else:
        print("Máy thắng! 🤖")

if __name__ == "__main__":
    main()
