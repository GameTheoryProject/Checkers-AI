from main import run_game
from checkers.constants import WHITE_NAME, WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE, RED_NAME
import tools

mm_baseline = ("minimax",4,3)
ab_baseline = ("alpha_beta",4,3)


# 计算不同深度的算法每一步平均时间
def t1():
    repeat_time = 10
    depths = [1,2,3,4,5]
    mm_avg_time = [0. for i in range(len(depths))]           # minimax times
    ab_avg_time = [0. for i in range(len(depths))]           # alpha_beta times

    for i in range(len(depths)):
        for e in range(repeat_time):
            print('generating: depths:{:2d}, repeat:{:3d}'.format(i,e))
            infos = run_game(*mm_baseline,"minimax",depths[i],3,first_strike=RED)
            mm_avg_time[i] += tools.get_avg_time(infos,RED_NAME)
            infos = run_game(*mm_baseline,"alpha_beta",depths[i],3,first_strike=RED)
            ab_avg_time[i] += tools.get_avg_time(infos,RED_NAME)

        mm_avg_time[i] /= repeat_time
        ab_avg_time[i] /= repeat_time

    with open('time_depths.txt', 'w') as f:
        f.write(str(depths)+'\n')
        f.write(str(mm_avg_time)+'\n')
        f.write(str(ab_avg_time)+'\n')
    pass

# 计算不同深度的alpha_beta算法的胜率
def t2():
    pass

# 计算使用不同eval函数的胜率，对手固定为(minimax,4,3)
def t3():
    pass

t1()
# t2()
# t3()
