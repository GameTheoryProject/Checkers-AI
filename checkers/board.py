import pygame
from .constants import BLACK, ROWS, COLS, WHITE, RED, SQUARE_SIZE, MAX_STEP, WHITE_NAME, RED_NAME, DRAW
from .piece import Piece

class Board:
    def __init__(self, turn):
        self.board = []
        self.red_left = self.white_left = (ROWS // 2 - 1) * (COLS // 2)
        self.red_kings = self.white_kings = 0
        self.create_board()
        self.step = 0
        self.turn = turn
    
    def draw_squares(self, win):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, WHITE, (col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))  # FIXED BUG

    def evaluate(self, color = WHITE, mode = 3):
        if mode == 1:
            value = self.white_left - self.red_left # 1
        elif mode == 2:
            value = self.white_left - self.red_left + (self.white_kings * 0.1 - self.red_kings * 0.1) # 2
        elif mode == 3:
            value = self.white_left - self.red_left + (self.white_kings * 0.5 - self.red_kings * 0.5) # 3
        elif mode == 4:
            value = self.white_left - self.red_left + (self.white_kings * 1 - self.red_kings * 1) # 4
        elif mode == 5:
            return self.heuristics(color) # 5
        else:
            assert(False)
        return value if color == WHITE else -value

    def heuristics(self, color):
        wp, rp = 0, 0           # white pawns, red pawns
        wk, rk = 0, 0           # white kings, red kings
        wc, rc = 0, 0           # white captures, red captures
        wkd, rkd = 0, 0         # white king distance, red king distance
        wsd, rsd = 0.0, 0.0     # white safer place, red safer place
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.get_piece(row, col)
                if piece:
                    r = row if row > (ROWS - (row + 1)) else (ROWS - (row + 1))
                    c = col if col > (COLS - (col + 1)) else (COLS - (col + 1))
                    d = int(((r ** 2.0 + c ** 2.0) ** 0.5) / 2.0)
                    if piece.color == WHITE:
                        wc += len(self.get_valid_moves(piece))
                        if piece.king:
                            wk += 1
                        else:
                            wp += 1
                            wkd += row + 1
                            wsd += d
                    else:
                        rc += len(self.get_valid_moves(piece))
                        if piece.king:
                            rk += 1
                        else:
                            rp += 1
                            rkd += ROWS - (row + 1)
                            rsd += d
        w1, w2, w3, w4 = 3., 2., 1., 1.
        if color == WHITE:
            white_count_heuristics = w1 * (((wp + wk * 2.0) - (rp + rk * 2.0)) / 1.0 + ((wp + wk * 2.0) + (rp + rk * 2.0)))
            white_capture_heuristics = w2 * ((wc - rc)/(1.0 + wc + rc))
            white_kingdist_heuristics = w3 * ((wkd - rkd)/(1.0 + wkd + rkd))
            white_safe_heuristics = w4 * ((wsd - rsd)/(1.0 + wsd + rsd))
            return white_count_heuristics + white_capture_heuristics \
                        + white_kingdist_heuristics + white_safe_heuristics
        else:
            red_count_heuristics = w1 * (((rp + rk * 2.0) - (wp + wk * 2.0)) / 1.0 + ((wp + wk * 2.0) + (rp + rk * 2.0)))
            red_capture_heuristics = w2 * ((rc - wc)/(1.0 + wc + rc))
            red_kingdist_heuristics = w3 * ((rkd - wkd)/(1.0 + wkd + rkd))
            red_safe_heuristics = w4 * ((rsd - wsd)/(1.0 + wsd + rsd))
            return red_count_heuristics + red_capture_heuristics \
                        + red_kingdist_heuristics + red_safe_heuristics


    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if row == ROWS - 1 or row == 0:
            if not piece.king:  # FIXED BUG
                piece.make_king()
                if piece.color == WHITE:
                    self.white_kings += 1
                else:
                    self.red_kings += 1

    def get_piece(self, row, col):
        return self.board[row][col]

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row +  1) % 2):
                    if row < ROWS // 2 - 1:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > ROWS // 2:
                        self.board[row].append(Piece(row, col, RED))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)
        
    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == RED:
                    self.red_left -= 1
                    self.red_kings -= 1 if piece.king else 0    # FIXED BUG
                else:
                    self.white_left -= 1
                    self.white_kings -= 1 if piece.king else 0  # FIXED BUG
    
    def winner(self):
        # 某一方无子而结束
        if self.red_left * self.white_left <= 0:
                return WHITE_NAME if self.red_left <= 0 else RED_NAME
        # 达到最大step而结束
        elif self.step >= MAX_STEP:
            return DRAW if self.relative_score() == 0 else \
                (WHITE_NAME if self.relative_score() > 0 else RED_NAME)
        # 当前执行方无法移动而结束
        else:
            pieces = self.get_all_pieces(self.turn)
            for p in pieces:
                if len(self.get_valid_moves(p)) > 0:
                    return None
            return RED_NAME if self.turn == WHITE else WHITE_NAME
        assert False

    def relative_score(self):
        # king得s分，非king得1分
        s = 2
        score = (self.white_kings*(s-1) + self.white_left) - (self.red_kings*(s-1) + self.red_left)
        # print(self.white_kings,self.white_left,self.red_kings,self.red_left)
        return score

    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == RED or piece.king:
            moves.update(self._traverse_left(row -1, max(row-3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row -1, max(row-3, -1), -1, piece.color, right))
        if piece.color == WHITE or piece.king:
            moves.update(self._traverse_left(row +1, min(row+3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row +1, min(row+3, ROWS), 1, piece.color, right))
    
        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break
            
            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, left-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, left+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1
        
        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break
            
            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r,right)] = last + skipped
                else:
                    moves[(r, right)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, right-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, right+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1
        
        return moves