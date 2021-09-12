import math


def no_round_sup(fn):
    return math.log(((fn+1)*5**.5 + (5*(fn+1)**2+4)**.5)/2, (1+5**.5)/2) - 2


def find_sup(fn):
    return math.floor(round(math.log(((fn+1)*5**.5 + (5*(fn+1)**2+4)**.5)/2, (1+5**.5)/2), 5)) - 2


def find_inf(fn):
    return math.floor(math.log(fn+1, 2))


def result(n):
    return find_sup(n) - find_inf(n)


def result_op(total_lambs):
    return math.floor(round(math.log(((total_lambs + 1) * 5 ** .5 + (5 * (total_lambs + 1) ** 2 + 4) ** .5) / 2, (1 + 5 ** .5) / 2), 5)) - 2 - math.floor(math.log(total_lambs+1, 2))


if __name__ == '__main__':
    print(result_op(143))