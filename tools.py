from checkers.constants import WHITE_NAME, WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE, RED_NAME


MAX_CONSIDERED = 100

def get_winner(infos):
    return infos[-1].split('winner:')[1].strip()


def get_total_time(infos, color, step):
    sum_time = 0
    for i in range(min(len(infos) - 1, 2 * step)):
        if infos[i].count(color):
            sum_time += float(infos[i].split('time:')[1])
    return sum_time


def get_avg_time(infos, color):
    num = (len(infos) - 1) // 2
    num += 1 if (len(infos) - 1) % 2 and infos[0].count(color) else 0
    # print(get_total_time(infos, color),num,get_total_time(infos, color) / num)

    if num > MAX_CONSIDERED:
        return get_total_time(infos, color, MAX_CONSIDERED) / MAX_CONSIDERED
    else:
        return get_total_time(infos, color, num) / num
