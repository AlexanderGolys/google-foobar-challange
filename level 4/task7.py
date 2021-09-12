POWERS_OF_TWO = {2**i for i in range(1, 32)}


def gcd(a_, b_):
    if a_*b_ == 0:
        return max(abs(a_), abs(b_))
    a = max(abs(a_), abs(b_))
    b = min(abs(a_), abs(b_))
    while b != 0:
        a, b = b, a % b
    return a


class IncidenceMatrix:
    def __init__(self, values):
        self.values = values
        self.delete_diagonal()

    def del_rows(self, *rows):
        for i in sorted(rows)[::-1]:
            del self.values[i]

    def del_cols(self, *cols):
        for i in sorted(cols)[::-1]:
            for row in self.values:
                del row[i]

    def remove_zeros(self):
        for i in range(len(self.values))[::-1]:
            if set(self.values[i]) == {0}:
                self.del_cols(i)
                self.del_rows(i)

    def __len__(self):
        return len(self.values)

    def least_connected_row(self):
        return min(enumerate(self.values), key=lambda x: sum(x[1]))[0]

    def any_connected_point(self, i):
        return next(j for j, x in enumerate(self.values[i]) if x == 1)

    def delete_diagonal(self):
        for i in range(len(self)):
            self.values[i][i] = 0


def can_be_connected(a, b):
    gcd_ab = gcd(a, b)
    a /= gcd_ab
    b /= gcd_ab
    return int(a+b not in POWERS_OF_TWO)


def solution(lst):
    incidence_matrix = IncidenceMatrix([[can_be_connected(a, b) for a in lst] for b in lst])
    return len(incidence_matrix) - no_pairs(incidence_matrix)


def no_pairs(matrix):
    print(matrix.values)
    matrix.remove_zeros()
    if len(matrix) == 0:
        return 0
    least_connected_row = matrix.least_connected_row()
    connected_point = matrix.any_connected_point(least_connected_row)
    matrix.del_rows(least_connected_row, connected_point)
    matrix.del_cols(least_connected_row, connected_point)
    return 2 + no_pairs(matrix)


if __name__ == '__main__':
    # print(solution([1, 1]))
    print(solution([1, 7, 3, 21, 13, 19]))





