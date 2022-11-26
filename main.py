# Assets: https://techwithtim.net/wp-content/uploads/2020/09/assets.zip
import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE
from checkers.game import Game
from minimax.algorithm import minimax, alpha_beta_search
import threading

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

# TODO
def win_thread():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)
    game.update()
    
    player_color = RED
    human_player = True
    AI_color = WHITE if player_color == RED else RED

    # t1 = threading.Thread(target=win_thread)
    # t1.start()

    while run:
        clock.tick(FPS)

        if game.turn == AI_color:
            value, new_board = minimax(game.get_board(), 5, AI_color, game)
            # value, new_board = alpha_beta_search(game.get_board(), 4, WHITE, game, [float('-inf'),float('inf')])
            game.ai_move(new_board)

        elif game.turn == player_color:
            if not human_player:
                value, new_board = minimax(game.get_board(), 4, player_color, game)
                game.ai_move(new_board)
            else:
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
        
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         run = False
            
        #     if event.type == pygame.MOUSEBUTTONDOWN:
        #         pos = pygame.mouse.get_pos()
        #         row, col = get_row_col_from_mouse(pos)
        #         game.select(row, col)

        game.update()

        print("step:{:4d}, winner:{}".format(step, winner))
        # print(game.board.white_kings,game.board.white_left,game.board.red_kings,game.board.red_left)
        if winner != None:
            run = False
            input("game over")

        # pygame.time.delay(1000)

    pygame.quit()

main()
