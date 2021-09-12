def parse(version):
    return list(map(int, version.split('.'))) + [-1]*(2-version.count('.'))


def task2(versions):
    return sorted(versions, key=parse)


if __name__ == '__main__':
    print(task2({"1.1.2", "1.0", "1.3.3", "1.0.12", "1.0.2"}))
