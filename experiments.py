from main import run_game
from checkers.constants import WHITE_NAME, WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE, RED_NAME
import tools

mm_baseline = ("minimax",4,3)
ab_baseline = ("alpha_beta",4,3)


# 计算不同深度的算法每一步平均时间
def t1():
    repeat_time = 10
    depths = [1,2,3,4,5,6,7,8]
    mm_avg_time = [0. for i in range(len(depths))]           # minimax times
    ab_avg_time = [0. for i in range(len(depths))]           # alpha_beta times

    for e in range(repeat_time):
        for i in range(len(depths)):
            print('generating: repeat:{:3d}, depths:{:2d}'.format(e, depths[i]), flush=True)
            infos = run_game(*mm_baseline,"minimax",depths[i],3,first_strike=RED,visual=False,exp1=True)
            mm_avg_time[i] += tools.get_avg_time(infos,RED_NAME)
            infos = run_game(*mm_baseline,"alpha_beta",depths[i],3,first_strike=RED,visual=False,exp1=True)
            ab_avg_time[i] += tools.get_avg_time(infos,RED_NAME)

        print(depths)
        print(mm_avg_time)
        print(ab_avg_time)

    for i in range(len(depths)):
        mm_avg_time[i] /= repeat_time
        ab_avg_time[i] /= repeat_time

    with open('exp1.time_depths.txt', 'w') as f:
        f.write(str(depths)+'\n')
        f.write(str(mm_avg_time)+'\n')
        f.write(str(ab_avg_time)+'\n')
    pass

# 计算不同深度的算法的胜率
def t2():
    repeat_time = 10
    red_depths = [1,2,3,4]
    white_depths = [1,2,3,4]

    red_win = [[0 for j in range(len(white_depths))] for i in range(len(red_depths))]

    for i in range(len(red_depths)):
        for j in range(len(white_depths)):
            for e in range(repeat_time):
                print('generating: red_depth:{:2d}, white_depth:{:2d}, repeat:{:3d}'.format(red_depths[i],white_depths[j],e), flush=True)
                infos = run_game("minimax",white_depths[j],3,"minimax",red_depths[i],3,first_strike=RED)
                red_win[i][j] += 1 if tools.get_winner(infos) == RED_NAME else 0

            red_win[i][j] /= repeat_time
    
    with open('exp2.win_rate_depths.txt', 'w') as f:
        for i in red_win:
            f.write(str(i)+'\n')
    pass

# 计算使用不同eval函数的胜率
def t3():
    repeat_time = 10
    red_mode = [1,2,3,4,5]
    white_mode = [1,2,3,4,5]

    red_win = [[0 for j in range(len(white_mode))] for i in range(len(red_mode))]
    for i in range(len(red_mode)):
        for j in range(len(white_mode)):
            for e in range(repeat_time):
                print('generating: red_mode:{:2d}, white_mode:{:2d}, repeat:{:3d}'.format(red_mode[i],white_mode[j],e), flush=True)
                infos = run_game("minimax",4,white_mode[j],"minimax",4,red_mode[i],first_strike=RED)
                red_win[i][j] += 1 if tools.get_winner(infos) == RED_NAME else 0

            red_win[i][j] /= repeat_time

    with open('exp3.win_rate_eval.txt', 'w') as f:
        for i in red_win:
            f.write(str(i)+'\n')
    pass

t1()

# t2()

# t3()
