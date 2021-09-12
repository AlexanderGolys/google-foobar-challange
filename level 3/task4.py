import functools
import operator
import copy
import itertools


def gcd(a_, b_):
    if a_*b_ == 0:
        return max(abs(a_), abs(b_))
    a = max(abs(a_), abs(b_))
    b = min(abs(a_), abs(b_))
    while b != 0:
        a, b = b, a % b
    return a


def multiple_gcd(*args):
    return functools.reduce(gcd, args)


@functools.total_ordering
class Fraction:
    def __init__(self, a, b):
        if b == 0:
            raise ValueError
        self.a = a
        self.b = b
        self.reduce()

    def reduce(self):

        if self.a == 0:
            self.b = 1
            return self

        if self.a * self.b < 0:
            self.a = -abs(self.a)
            self.b = abs(self.b)
        else:
            self.a = abs(self.a)
            self.b = abs(self.b)

        while gcd(self.a, self.b) != 1:
            gcd_ab = gcd(self.a, self.b)
            self.a //= gcd_ab
            self.b //= gcd_ab

        if self.a % self.b == 0:
            self.a //= self.b
            self.b = 1

        if self.b % self.a == 0:
            self.b //= self.a
            self.a = 1

        return self

    # @functools.singledispatchmethod
    def __add__(self, other):
        if isinstance(other, int):
            other = Fraction(other, 1)
        return Fraction(self.a * other.b + self.b * other.a, other.b * self.b).reduce()

    # @__add__.register(int)
    # def _(self, other):
    #     return self + Fraction(other, 1)

    def __neg__(self):
        return Fraction(-self.a, self.b).reduce()

    # @functools.singledispatchmethod
    def __mul__(self, other):
        if isinstance(other, int):
            other = Fraction(other, 1)
        return Fraction(self.a * other.a, self.b * other.b).reduce()

    # @__mul__.register(int)
    # def _(self, other):
    #     return Fraction(self.a * other, self.b).reduce()

    def __invert__(self):
        return Fraction(self.b, self.a).reduce()

    # def __str__(self):
    #     return f'{self.a}/{self.b}'

    def __abs__(self):
        return Fraction(abs(self.a), abs(self.b)).reduce()

    # @functools.singledispatchmethod
    def __eq__(self, other):
        if isinstance(other, int):
            other = Fraction(other, 1)
        self.reduce()
        other.reduce()
        return self.a == other.a and self.b == other.b

    # @__eq__.register(int)
    # def _(self, other):
    #     self.reduce()
    #     return self.a == other and self.b == 1

    # @functools.singledispatchmethod
    def __gt__(self, other):
        if isinstance(other, int):
            other = Fraction(other, 1)
        return not self == other and self.a / self.b > other.a / other.b

    # @__gt__.register(int)
    # def _(self, other):
    #     return not self == other and self.a / self.b > other

    # @functools.singledispatchmethod
    def __truediv__(self, other):
        if isinstance(other, int):
            other = Fraction(other, 1)
        return self * ~other

    # @__truediv__.register(int)
    # def _(self, other):
    #     return Fraction(self.a, self.b * other)

    def __sub__(self, other):
        return self + -other

    def to_common_divisor(self, other):
        gcd_ = gcd(self.b, other.b)
        return Fraction(self.a*other.b/gcd_, self.b*other.b/gcd_), Fraction(other.a*self.b/gcd_, self.b*other.b/gcd_)


class Matrix:
    def __init__(self, values):
        self.values = values

    def __len__(self):
        return len(self.values)

    def __mul__(self, other):
        return Matrix(list(map(lambda row: [a * other for a in row], self.values)))

    def __getitem__(self, item):
        return self.values[item[0]][item[1]]

    def del_row(self, i):
        del self.values[i]

    def del_col(self, i):
        for row in self.values:
            del row[i]

    def transpose(self):
        return Matrix(list(zip(*self.values)))

    def adjugate(self):
        return Matrix(
            [[self.minor(j, i) * (-1) ** (i + j) for i in range(len(self))] for j in range(len(self))]).transpose()

    def is_squared(self):
        return len(self) == len(self.values[0])

    def minor(self, i, j):
        if not self.is_squared():
            raise ValueError('Matrix is not squared.')
        m = Matrix(copy.deepcopy(self.values))
        m.del_row(i)
        m.del_col(j)
        if len(m) == 1:
            return m[0, 0]
        return m.determinant()

    def determinant(self):
        if not self.is_squared():
            raise ValueError('Matrix is not squared.')
        if len(self) == 1:
            return self[0, 0]
        if len(self) == 2:
            return self[0, 0]*self[1, 1] - self[0, 1]*self[1, 0]
        return functools.reduce(operator.add, [a * self.minor(0, j) * (-1) ** j for j, a in enumerate(self.values[0])])

    def __invert__(self):
        if not self.is_squared():
            raise ValueError('Matrix is not squared.')
        if len(self) == 1:
            return self.__class__([[self[0, 0].__invert__()]])
        return self.adjugate() * (~self.determinant())

    # def __str__(self):
    #     return '\n'.join(['| ' + ' '.join([str(el) for el in row]) + ' |' for row in self.values])

    def flip_rows(self, i, j):
        self.values[i], self.values[j] = self.values[j], self.values[i]

    def flip_columns(self, i, j):
        for row in self.values:
            row[i], row[j] = row[j], row[i]

    def __sub__(self, other):
        values = [[a-b for a, b in zip(row1, row2)] for row1, row2 in zip(self.values, other.values)]
        return Matrix(values)

    def get_row(self, i):
        return self.values[i]

    def get_column(self, i):
        return [row[i] for row in self.values]

    def __matmul__(self, other):
        values = [[functools.reduce(operator.add, [a*b for a, b in zip(self.get_row(i), other.get_column(j))])
                   for i in range(len(self))] for j in range(len(other.values[0]))]
        return Matrix(values)


class IdentityMatrix(Matrix):
    def __init__(self, n):
        values = [[Fraction(int(i == j), 1) for i in range(n)] for j in range(n)]
        # super().__init__(values)
        self.values = values


class AbsorbingMarkovChainMatrix(Matrix):
    def zeros_on_bottom(self):
        return len(list(itertools.groupby(self.values, lambda row: set(row) == {0}))) <= 2

    def __init__(self, values):
        # super().__init__(values)
        self.values = values

        self.remove_not_connected_components()

        for i, row in enumerate(self.values):
            if row[i] == 1 and set(row[:i]).union(set(row[i+1:])) == {0}:
                row[i] = 0

        while not self.zeros_on_bottom():
            for i, row in enumerate(self.values):
                if i > 0 and set(row) != {0} and set(self.values[i - 1]) == {0}:
                    self.flip_rows(i, i - 1)
                    self.flip_columns(i, i - 1)

        self.no_absorbing_states = sum([int(set(row) == {0}) for row in self.values])

        for i, row in enumerate(self.values):
            row_sum = sum(row)
            if row_sum != 0:
                for j in range(len(row)):
                    row[j] = Fraction(row[j], row_sum)

            else:
                for j in range(len(row)):
                    row[j] = Fraction(int(i == j), 1)

    def remove_not_connected_components(self):
        connected_rows = self.connected_rows(0).union({0})
        for _ in range(10):
            for r in connected_rows:
                connected_rows = connected_rows.union(self.connected_rows(r))

        not_connected_rows = set(range(len(self))) - connected_rows
        sorted_not_connected_rows = sorted(list(not_connected_rows), reverse=True)

        for r in sorted_not_connected_rows:
            if set(self.values[r]) != {0}:
                self.del_row(r)
                self.del_col(r)

    def connected_rows(self, row_number):
        return {i for i, v in enumerate(self.values[row_number]) if v != 0}

    def fundamental_matrix(self):
        no_transient_states = len(self) - self.no_absorbing_states
        submatrix_values = list(map(lambda row: row[:no_transient_states], self.values[:no_transient_states]))
        return (IdentityMatrix(no_transient_states) - Matrix(submatrix_values)).__invert__()

    def absorbing_probabilities(self):
        no_transient_states = len(self) - self.no_absorbing_states
        R = Matrix(list(map(lambda row: row[no_transient_states:], self.values[:no_transient_states])))
        return self.fundamental_matrix().__matmul__(R)

    def zero_state_absorbing_probabilities(self):
        return self.absorbing_probabilities().get_column(0)


def reformat_result(prob):
    for i, f in prob[1:]:
        prob[0], prob[i+1] = prob[0].to_common_divisor(f)
    result = list(map(lambda f: f.a, prob)) + [prob[0].b]
    return result


def handle_zero_row(m):
    no_zero_rows = len([1 for i, row in enumerate(m) if set(row[:i] + row[i+1:]) == {0}]) - 1
    return [1] + [0]*no_zero_rows + [1]


def solution(m):
    if set(m[0]) == {0}:
        return handle_zero_row(m)
    matrix = AbsorbingMarkovChainMatrix(m)
    raw_result = matrix.zero_state_absorbing_probabilities()
    return reformat_result(raw_result)


if __name__ == '__main__':
    print(solution([[432, 234, 44, 2, 3], [342, 2342, 342, 234, 5], [2, 23, 234, 22, 44], [121, 5, 0, 0, 111], [0, 0, 0, 0, 0]]))
    # print(solution([[1, 1, 1, 1, 1,],  [0, 0, 0, 0, 0,], [1, 1, 1, 1, 1,], [0, 0, 0, 0, 0,], [1, 1, 1, 1, 1,]]))
    # m1 = Matrix([[0, 0, 0], [4, 5, 6]])
    # m2 = Matrix([[0, 0], [1, 2], [2, 2]])
    # print(m1 @ m2)
