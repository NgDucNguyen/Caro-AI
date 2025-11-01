'''
import os, sys, json
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

# ensure src is on sys.path so `from backend import engine` works
PROJECT_ROOT = str(Path(__file__).resolve().parents[2])  # d:\Project\IntroAI\Caro-AI
SRC_DIR = os.path.join(PROJECT_ROOT, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from backend import engine

FRONTEND_DIR = os.path.dirname(__file__)
HTML_PATH = os.path.join(FRONTEND_DIR, "uiInGame.html")

def state_dict():
    return {
        "board": engine.board,
        "player_turn": engine.player_turn,
        "game_over": engine.game_over,
        "winner_text": engine.winner_text,
        "highlight_cells": engine.highlight_cells,
        "scores": engine.scores,
        "move_history": engine.move_history,
    }

class Handler(BaseHTTPRequestHandler):
    def _send_json(self, obj, code=200):
        data = json.dumps(obj).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _read_json(self):
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            return {}
        body = self.rfile.read(length)
        return json.loads(body.decode("utf-8"))

    def do_GET(self):
        if self.path == "/" or self.path.startswith("/uiInGame.html"):
            try:
                with open(HTML_PATH, "rb") as f:
                    html = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(html)))
                self.end_headers()
                self.wfile.write(html)
            except FileNotFoundError:
                self.send_response(404); self.end_headers()
        elif self.path == "/state":
            self._send_json(state_dict())
        else:
            self.send_response(404); self.end_headers()

    def do_POST(self):
        if self.path == "/move":
            data = self._read_json()
            idx = data.get("index")
            if not isinstance(idx, int) or not (0 <= idx <= 8):
                return self._send_json({"ok": False, "error": "invalid index"}, 400)
            accepted = engine.apply_player_move(idx)
            if accepted and (not engine.game_over) and (not engine.player_turn):
                engine.apply_ai_move()
            return self._send_json(state_dict())
        elif self.path == "/ai":
            engine.apply_ai_move()
            return self._send_json(state_dict())
        elif self.path == "/reset":
            engine.reset_game()
            return self._send_json(state_dict())
        elif self.path == "/undo":
            engine.undo()
            return self._send_json(state_dict())
        else:
            self.send_response(404); self.end_headers()

def run(host="127.0.0.1", port=5000):
    server = HTTPServer((host, port), Handler)
    print(f"Serving on http://{host}:{port}/ - press Ctrl+C to stop")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Stopping server")
        server.server_close()

if __name__ == "__main__":
    run()
'''