# Assets: https://techwithtim.net/wp-content/uploads/2020/09/assets.zip
import copy
import pygame
from checkers.constants import WHITE_NAME, WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE, RED_NAME
from checkers.game import Game
from minimax.algorithm import minimax, alpha_beta_search
import random
import time

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def sample_one(boards):
    return random.sample(list(boards), 1)[0]

def AI_calc(game, color, AI, depth, eval_mode):
    start = time.time()
    if AI == "minimax":
        value, new_boards = minimax(game.get_board(), depth, color,  game, evaluate_mode=eval_mode)
    elif AI == "alpha_beta":
        value, new_boards = alpha_beta_search(game.get_board(), depth, color,  game, [float('-inf'),float('inf')], evaluate_mode=eval_mode)
    else:
        assert False
    calc_time = time.time()-start
    return value, sample_one(new_boards), calc_time

def run_game(WHITE_AI, WA_depth, WA_eval_mode, RED_AI, RA_depth, RA_eval_mode, first_strike = RED, visual = True, exp1 = False):
    if visual:
        FPS = 60
        WIN = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Game Theory Project: Checkers-AI')
        clock = pygame.time.Clock()
        game = Game(WIN, first_strike)  # the first turn color
    else:
        game = Game(None, first_strike)
    
    game.update()
    run = True
    all_infos = []
    human_player = False

    while run:
        if visual:
            clock.tick(FPS)
        turn = WHITE_NAME if game.turn == WHITE else RED_NAME

        if game.turn == WHITE:
            value, new_board, calc_time = AI_calc(game, WHITE, WHITE_AI, WA_depth, WA_eval_mode)
            game.ai_move(new_board)

        elif game.turn == RED:
            if not human_player:
                value, new_board, calc_time = AI_calc(game, RED, RED_AI, RA_depth, RA_eval_mode)
                game.ai_move(new_board)
            else:
                if not visual: assert False
                while True:
                    out = False
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            pos = pygame.mouse.get_pos()
                            row, col = get_row_col_from_mouse(pos)
                            if not game.select(row, col):
                                out = True
                    game.update()
                    if out: break
        else:
            assert False

        step, winner = game.check_winner()
        
        game.update()

        info1 = "step:{:5d}, turn:{}, time:{:.5f}".format(step, turn.ljust(5,' '), calc_time)
        all_infos.append(info1)
        # print(info1)
        if winner != None:
            run = False
            info2 = "game over, winner:{}".format(winner.ljust(5,' '))
            all_infos.append(info2)
            # print(info2)
            # input()

        # enable for exp1, for saving time
        # ---------------------------------------------
        if exp1 and game.step >= 100:
            run = False
            info2 = "stop running"
            all_infos.append(info2)
        # ---------------------------------------------

        # pygame.time.delay(1000)

    if visual:
        pygame.quit()

    return all_infos

# x = run_game("minimax",4,3,"minimax",4,3,first_strike=RED)
# print(x)

if __name__ == '__main__':
    pass