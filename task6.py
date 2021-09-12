def solution(lst):
    result = 0
    for i, n in enumerate(lst[1:-1]):
        lower = len([x for x in lst if n % x == 0])
        upper = len([x for x in lst[i + 2:] if x % n == 0])
        result += lower * upper
    return result


if __name__ == '__main__':
    print(solution([1, 1, 1]))

    print(solution([1, 2, 3, 4, 5, 6,]))

    print(solution(list(range(100, 2000, 100))))

