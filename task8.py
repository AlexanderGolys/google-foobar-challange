import itertools
import math

import itertools
import math

# def combinations(s, n):


def bellman_ford(matrix, vertex):
    result = [0xFFFFFFFF]*len(matrix)
    result[vertex] = 0
    return bellman_ford_rec(vertex, result, matrix, set())


def bellman_ford_rec(vertex, result, matrix, path):
    if vertex in path:
        return
    for i in range(len(matrix)):
        if result[vertex] + matrix[vertex][i] < result[i]:
            result[i] = result[vertex] + matrix[vertex][i]
            if bellman_ford_rec(i, result, matrix, path.union({vertex})) is None:
                return
    return result


def try_permutation(matrix, permutation, threshold):
    # print(f'trying permutation {list(permutation)} (result: {sum([matrix[i][j] for i, j in zip(permutation[:-1], permutation[1:])])})')
    return sum([matrix[i][j] for i, j in zip(permutation[:-1], permutation[1:])]) <= threshold


def try_combination(matrix, combination, threshold):
    # print(f'trying combination {tuple(combination)}')
    for permutation in itertools.permutations(combination):
        if try_permutation(matrix, [0] + list(permutation) + [len(matrix)-1], threshold):
            return list(permutation)


def try_n_bunnies(matrix, n, threshold):
    result = []
    for combination in itertools.combinations(range(1, len(matrix) - 1), n):
        partial_result = try_combination(matrix, combination, threshold)
        if partial_result is not None:
            result.append(partial_result)
    return result


def solution(matrix, threshold):
    shortest_path_matrix = [bellman_ford(matrix, i) for i in range(len(matrix))]
    print(shortest_path_matrix)
    if None in shortest_path_matrix:
        return list(range(len(matrix) - 2))
    for no_bunnies in range(1, len(matrix) - 1)[::-1]:
        result = try_n_bunnies(shortest_path_matrix, no_bunnies, threshold)
        if result:
            return list(map(lambda x: x-1, sorted(list(set(sum(result, []))))[:no_bunnies]))
    return []










if __name__ == '__main__':
    print solution([[0, 2, 2, 2, 70, 7, 3], [33, 24, 23, 23, 34, 73, 33], [0, 2, 2, 2, 30, 7, 3], [0, 2, 2, 2, -1, 7, 3], [0, 2, 2, 2, 33, 7, 3], [0, 2, 2, 2, 3, 7, 3], [0, 2, 2, 2, 0, 7, 3]], 4)
    print solution([[0, -1, 1, 1, 1], [-1, 0, 1, 1, 1], [1, 1, 0, 1, 1], [1, 1, 1, 0, 1], [1, 1, 1, 9999999, 0]], 999)
    print solution([[0, 1, 1, 1], [10, 10, 10, 1], [1, 1, 1, 1], [10, 10, 10, 10]], 2)







