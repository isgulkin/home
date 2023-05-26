from itertools import combinations
import numpy as np

n, k = map(int, input('n k\n').split())


def make_G(P, k):
    G = np.hstack((np.eye(k), P))
    return G.astype(int)


P_list = []
for i in range(k):
    P_list.append(np.vectorize(int)([i for i in input(f'{i + 1} строка\n')]))
P = np.concatenate([P_list])
G = make_G(P, k)
u = np.vectorize(int)([i for i in input(f'введите слово-вектор для кодировки длинной k\n')])


def make_H(G):
    k, n = G.shape
    P = G[:, k:]
    H = np.hstack((-P.T % 2, np.eye(n - k)))
    return H.astype(int)


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


def decode_slepian(v, table, q):
    n, k = table.shape[0:2]
    for i in range(n):
        for j in range(k):
            if np.array_equal(v, table[i][j]):
                return (v - table[i][0]) % q


def generate_syndrome_table(table, H):
    syndrome_table = []
    for line in table:
        syndrome = np.dot(line[0], H.T) % 2
        syndrome_line = [line[0]] + [syndrome]
        syndrome_table.append(syndrome_line)
    return np.array(syndrome_table, dtype=object)


def decode_syndrome(v, G, table, q):
    H = make_H(G)
    s = v @ H.T % q
    if np.count_nonzero(s) == 0:
        return v
    for line in table:
        if np.array_equal(s, line[0] @ H.T % q):
            weight_line = list(map(np.count_nonzero, line))
            l = weight_line[0]
            e = line[0]
            for i in range(1, len(weight_line)):
                if weight_line[i] <= l:
                    return 'отказ от декодирования'
            return (v - e) % q


H = make_H(G)
print('H.T\n', H.T)
print('H\n', H)
table = generate_table(G)
print('таблица стандартного расположения')
for line in table:
    for el in line:
        print(el, end='')
    print('\n')
print('таблица синдромов')
syn_table = generate_syndrome_table(table, H)
for line in syn_table:
    for el in line:
        print(el, end='')
    print('\n')
print('закодированное сообщение', u @ G % 2)
noised = np.vectorize(int)([i for i in input('Введите вектор с ошибкой длинной n\n')])
print('Синдром зашумленного сообщения', noised @ H.T % 2)
