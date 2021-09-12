"""
This might require an explanation.

The Rayleigh's theorem is used here - for every Beatty sequence {an} = {floor(nx)}, where x is irrational, there is
a complement sequence bn such that {an}u{bn}=N.

This reduces the computation of a(n) to the computation of a(floor(n/(2 + sqrt(2)), so the complexity in log n.
"""
import decimal

decimal.getcontext().prec = 101


def solution(n):
    n = int(n)
    if n < 10:
        return str(sum([int(i*decimal.Decimal(2).sqrt()) for i in range(n+1)]))
    m = new_index(n)
    return str(int(n*decimal.Decimal(2).sqrt())*(int(n*decimal.Decimal(2).sqrt())+1)/2 - m*(m+1) - int(solution(m)))


def new_index(n):
    return int(int(n*decimal.Decimal(2).sqrt())/(decimal.Decimal(2).sqrt() + 2))


if __name__ == '__main__':
    k = int(int(1e100))
    k_str = str(k)

    print(solution(k_str))
    print(sum([int(c*2**.5) for c in range(1, k+1)]))
