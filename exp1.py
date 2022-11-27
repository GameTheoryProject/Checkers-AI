from main import run_game
from checkers.constants import WHITE_NAME, WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE, RED_NAME

mm_baseline = ("minimax",4,3)
ab_baseline = ("alpha_beta",4,3)

# 计算不同深度的算法每一步平均时间
def t1():
    depths = [1,2,3,4,5,6]
    times_m = []    # minimax times
    tims_a = []     # alpha_beta times

    for d in depths:
        run_game(*mm_baseline,"minimax",d,3,first_strike=RED)


    # TODO visualization

    pass

t1()