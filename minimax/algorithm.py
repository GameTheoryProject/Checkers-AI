from copy import deepcopy
import pygame

RED = (255,0,0)
WHITE = (255, 255, 255)

def minimax(position, depth, color, game, evaluate_mode = 3, max_player = True):
    if depth == 0 or position.winner() != None:
        return position.evaluate(color, evaluate_mode), position
    
    if max_player:
        maxEval = float('-inf')
        best_move = None
        for move in get_all_moves(position, color, game):
            evaluation = minimax(move, depth-1, color, game, evaluate_mode, False)[0]
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                best_move = move
        
        return maxEval, best_move
    else:
        minEval = float('inf')
        best_move = None
        for move in get_all_moves(position, other_color(color), game):
            evaluation = minimax(move, depth-1, color, game, evaluate_mode, True)[0]
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move = move
        
        return minEval, best_move


def alpha_beta_search(position, depth, color, game, a_b, evaluate_mode = 3, max_player = True):
    # 当到达最后一层且此时可以分出胜负时
    if depth == 0 or position.winner() != None:
        return position.evaluate(color, evaluate_mode), position

    if max_player:
        maxEval = float('-inf')
        best_move = None
        for move in get_all_moves(position, color, game):
            evaluation = alpha_beta_search(move, depth-1, color, game, a_b, evaluate_mode, False)[0]
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                best_move = move
            # alpha-beta 剪枝
            if maxEval >= a_b[0] and maxEval <= a_b[1]:
                a_b[0] = maxEval
            elif maxEval > a_b[1]:
                # print("Pruning!")
                break

        return maxEval, best_move
    else:
        minEval = float('inf')
        best_move = None
        for move in get_all_moves(position, other_color(color), game):
            evaluation = alpha_beta_search(move, depth-1, color, game, a_b, evaluate_mode, True)[0]
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move = move
            # alpha-beta 剪枝
            if minEval >= a_b[0] and minEval <= a_b[1]:
                a_b[1] = minEval
            elif minEval < a_b[0]:
                # print("Pruning!")
                break

        return minEval, best_move


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