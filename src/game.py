import numpy as np

class Game:
    def __init__(self):
        #khoi tao trang thai ban dau cua tro choi
        self.board = self._create_board()
        self.current_player = 'X'
        self.game_over = False
        self.winner = None
    
    #khoi tao bang choi 
    def _create_board(self):
        return np.array([['']*3 for _ in range(3)])
    
    # kiem ra xem nuoc di co hop le ko
    def is_valid_move(self, row, col):
        return 0<=row<3 and 0<=col<3 and self.board[row][col] == ''
    
    #thuc hien buoc choi va cap nhat
    def make_move(self,row,col):
        if not self.game_over and self.is_valid_move(row,col):
            self.board[row][col] = self.current_player
            
            #kiem tra thang/hoa
            if self._check_win(self.current_player):
                self.game_over = True
                self.winner = self.current_player
            elif self._check_draw(self.current_player):
                 self.game_over = True
                 self.winner = "Draw"
                 
            #Chuyen luot neu game chua ket thuc
            if not self.game_over:
                #chuyen luot X sang O
                self.current_player = 'O' if self.current_player == 'X' else 'X'
            
            return True #nuoc di thanh cong
        return False
    
    #kiem tra thang
    def _check_win(self,player):
        for i in range(3):
            if np.all(self.board[i,:]==player): return True #check hang
            if np.all(self.board[:, i] == player): return True #check cot
        #check duong cheo
        if np.all(np.dia(self.board)==player): return True
        #duong cheo phu
        if np.all(np.diag(np.fliplr(self.board))==player): return True
        return False
    
    #kiem tra hoa
    def _check_draw(self):
        is_full = not np.any(self.board == '') #ko con o trong nao
        
        # Tra True neu bang day va ko co nguoi thang
        return is_full and not not self._check_win('X') and not self._check_win('O')
    
    #dat lai chuong trinh de choi lai
    def reset_game(self):
        self.board = self._create_board()
        self.current_player = 'X'
        self.game_over = False
        self.winner = None
        print("Game da duoc lam moi!")
        