from copy import deepcopy
import copy
import random
import pygame

RED = (255,0,0)
WHITE = (255, 255, 255)

def minimax(position, depth, color, game, evaluate_mode = 3, max_player = True):
    if depth == 0 or position.winner() != None:
        return position.evaluate(color, evaluate_mode), position
    
    if max_player:
        maxEval = float('-inf')
        best_move = None
        best_moves = []
        for move in get_all_moves(position, color, game):
            evaluation = minimax(move, depth-1, color, game, evaluate_mode, False)[0]
            if evaluation > maxEval:
                best_moves = []
                best_moves.append(move)
                maxEval = evaluation
            elif evaluation == maxEval:
                best_moves.append(move)
            else:
                pass
        # best_move = best_moves[random.randint(0, len(best_moves) - 1)] if len(best_moves) > 0 else None

        return maxEval, best_moves
    else:
        minEval = float('inf')
        best_move = None
        best_moves = []
        for move in get_all_moves(position, other_color(color), game):
            evaluation = minimax(move, depth-1, color, game, evaluate_mode, True)[0]
            if evaluation < minEval:
                best_moves = []
                best_moves.append(move)
                minEval = evaluation
            elif evaluation == minEval:
                best_moves.append(move)
            else:
                pass
        # best_move = best_moves[random.randint(0, len(best_moves) - 1)] if len(best_moves) > 0 else None
        
        return minEval, best_moves


def alpha_beta_search(position, depth, color, game, a_b, evaluate_mode = 3, max_player = True):
    # 当到达最后一层且此时可以分出胜负时
    if depth == 0 or position.winner() != None:
        return position.evaluate(color, evaluate_mode), position

    if max_player:
        maxEval = float('-inf')
        best_move = None
        best_moves = []
        for move in get_all_moves(position, color, game):
            evaluation = alpha_beta_search(move, depth-1, color, game, copy.deepcopy(a_b), evaluate_mode, False)[0]
            if evaluation > maxEval:
                best_moves = []
                best_moves.append(move)
                maxEval = evaluation
            elif evaluation == maxEval:
                best_moves.append(move)
            else:
                pass
            
            # alpha-beta 剪枝
            a_b[0] = max(a_b[0], maxEval)
            if a_b[1] < a_b[0]:
                # print("Pruning!")
                break
        # best_move = best_moves[random.randint(0, len(best_moves) - 1)] if len(best_moves) > 0 else None

        return maxEval, best_moves
    else:
        minEval = float('inf')
        best_move = None
        best_moves = []
        for move in get_all_moves(position, other_color(color), game):
            evaluation = alpha_beta_search(move, depth-1, color, game, copy.deepcopy(a_b), evaluate_mode, True)[0]
            if evaluation < minEval:
                best_moves = []
                best_moves.append(move)
                minEval = evaluation
            elif evaluation == minEval:
                best_moves.append(move)
            else:
                pass

            # alpha-beta 剪枝
            a_b[1] = min(a_b[1], minEval)
            if a_b[1] < a_b[0]:
                # print("Pruning!")
                break
        # best_move = best_moves[random.randint(0, len(best_moves) - 1)] if len(best_moves) > 0 else None
        
        return minEval, best_moves


def simulate_move(piece, move, board, game, skip):
    board.move(piece, move[0], move[1])
    if skip:
        board.remove(skip)

    return board

# 获取当前棋盘下某种颜色所有可能的行动，以新棋盘的形式存储
def get_all_moves(board, color, game):
    moves = []

    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        for move, skip in valid_moves.items():
            # draw_moves(game, board, piece)
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, game, skip)
            moves.append(new_board)
    
    return moves


def draw_moves(game, board, piece):
    valid_moves = board.get_valid_moves(piece)
    board.draw(game.win)
    pygame.draw.circle(game.win, (0,255,0), (piece.x, piece.y), 50, 5)
    game.draw_valid_moves(valid_moves.keys())
    pygame.display.update()
    #pygame.time.delay(100)

def other_color(color):
    return WHITE if color == RED else RED