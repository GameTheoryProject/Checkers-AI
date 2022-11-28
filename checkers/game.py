import pygame
from .constants import RED, WHITE, BLUE, SQUARE_SIZE
from checkers.board import Board

class Game:
    def __init__(self, win, turn):
        self._init(turn)
        self.win = win
        self.step = 0
        self.winner = None
    
    def update(self):
        if self.win:
            self.board.draw(self.win)
            self.draw_valid_moves(self.valid_moves)
            pygame.display.update()

    def _init(self, turn):
        self.selected = None
        self.turn = turn
        self.board = Board(self.turn)
        self.valid_moves = {}

    def check_winner(self):
        self.winner = self.board.winner()
        # print(self.board.white_kings,self.board.white_left,self.board.red_kings,self.board.red_left)
        # print("step:{:4d}, winner:{}".format(self.step, self.winner))
        return self.step, self.winner

    def reset(self):
        self._init()

    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)
        
        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True
            
        return False

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
        else:
            return False

        return True

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 15)

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == RED:
            self.turn = WHITE
        else:
            self.turn = RED
        self.board.turn = self.turn
        self.step += 1
        self.board.step += 1
        # self.check_winner()

    def get_board(self):
        return self.board

    def ai_move(self, board):
        self.board = board
        self.change_turn()