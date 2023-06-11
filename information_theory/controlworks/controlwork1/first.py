from typing import Union
import numpy as np
from itertools import combinations
import time

n, k = map(int, input('n k\n').split())
f = 2


def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Время выполнения функции {func.__name__}: {end_time - start_time:.5f} секунд")
        return result

    return wrapper


def canonical_matrix(p: np.array, k: int) -> np.array:
    return np.hstack((np.identity(k, dtype=int), p))


p_list = []
for i in range(k):
    p_list.append(np.vectorize(int)([i for i in input(f'{i + 1} строка\n')]))

p = np.concatenate([p_list])
g = canonical_matrix(p, k)

u = np.vectorize(int)([i for i in input(f'введите слово-вектор для кодировки длинной k\n')])


def check_matrix(g: np.array, field: int) -> np.array:
    k, n = g.shape
    return np.hstack((np.mod(-g[:, k:].T, field), np.identity(n - k, dtype=int)), dtype=int)


def generate_new_error_vector(table):
    n = table[0].shape[1]
    table_set = set(map(tuple, np.unique(np.vstack(table), axis=0)))
    for weight in range(1, n + 1):
        for vector in combinations(range(n), weight):
            new_vector = np.zeros(n, dtype=int)
            new_vector[list(vector)] = 1
            new_vector = np.mod(new_vector, 2)
            if tuple(new_vector) not in table_set:
                return new_vector
    return None


def generate_table(g: np.array) -> np.array:
    k, n = g.shape
    all_vectors = np.stack(np.meshgrid(*[range(2) for _ in range(k)])).T.reshape(-1, k)
    syndrome_vectors = np.mod(all_vectors @ g, 2)
    line = syndrome_vectors.reshape(2 ** k, n)
    table = np.array([line])
    error_vector = generate_new_error_vector(table)
    while error_vector is not None:
        table = np.append(table, [np.mod(error_vector + line, 2)], axis=0)
        error_vector = generate_new_error_vector(table)
    return table


def generate_syndrome_table(table, H):
    syndrome_table = []
    for line in table:
        syndrome = np.dot(line[0], H.T) % 2
        syndrome_line = [line[0]] + [syndrome]
        syndrome_table.append(syndrome_line)
    return np.array(syndrome_table, dtype=object)


@timer
def decode_syndrome(table: np.array, vector: np.array, g: np.array, field) -> Union[str, np.array]:
    h = check_matrix(g, field)
    s = np.mod(vector @ h.T, field)
    if np.count_nonzero(s) == 0:
        return vector

    syndrome_products = np.mod(table[:, 0] @ h.T, field)
    matched_indices = np.where(np.all(s == syndrome_products, axis=-1))[0]

    if matched_indices.size == 0:
        return 'Отказ от декодирования'

    matched_line = table[matched_indices[0]]
    weight_line = np.count_nonzero(matched_line, axis=1)
    min_weight = weight_line[0]
    e = matched_line[0]

    if np.any(weight_line[1:] <= min_weight):
        return 'Отказ от декодирования'

    return np.mod(vector - e, field)


h = check_matrix(g, f)
print('H.T\n', h.T)
print('H\n', h)

table = generate_table(g)
print('Таблица стандартного расположения')
for line in table:
    for el in line:
        print(el, end='')
    print('\n')

print('Таблица синдромов')
syn_table = generate_syndrome_table(table, h)
for line in syn_table:
    for el in line:
        print(el, end='')
    print('\n')

print('Закодированное сообщение', np.mod(u @ g, 2))

noised = np.vectorize(int)([i for i in input('Введите вектор с ошибкой длинной n\n')])
print('Синдром зашумленного сообщения', np.mod(noised @ h.T, 2))
