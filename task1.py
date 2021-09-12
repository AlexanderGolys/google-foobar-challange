def task1(l, n):
    return list(filter(lambda x: l.count(x) <= n, l))

def parse(version):
    return list(map(int, version.split('.')))

if __name__ == '__main__':
    l = [1, 2, 2, 3, 6, 4, 4, 7, 1]
    print(task1(l, 1))