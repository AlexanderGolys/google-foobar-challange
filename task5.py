def solution(a, b):
    i = 0
    a, b = int(a), int(b)
    while a*b != 0:
        if a == 1:
            return i + b - 1
        if b == 1:
            return i + a - 1
        i += max(a, b) // min(a, b)
        a, b = max(a, b) % min(a, b), min(a, b)
    return 'impossible'


if __name__ == '__main__':
    print(solution('4', '7'))