import numpy as np
from numpy.polynomial import Polynomial

np.polynomial.set_default_printstyle('unicode')

# n = int(input())  # длина кодового слова
# k = int(input())  # размерность кода
# d = int(input())  # минимальное кодовое расстояние
n, k, d = map(int, input('n k d\n').split())


def pretty_print(polynomial):
    terms = []
    for power, coeff in enumerate(polynomial.coef):
        if np.abs(coeff) > 1e-9:
            terms.append(f"{coeff:.1f}·x^{power}")
    print(" + ".join(terms))


def generate_f_vector(n):
    return np.concatenate(([1], np.zeros(n - 1), [1]))


def cyclic_matrix(vector, num_rows, num_cols):
    matrix = np.zeros((num_rows, num_cols), dtype=int)
    for i in range(num_rows):
        matrix[i] = np.roll(vector, i)
    return matrix


def zeroes(vector):
    return np.mod(np.concatenate((vector, np.zeros(n - len(vector), dtype=int))), 2).astype(int)


def encode(g, u):
    gu = np.polymul(np.poly1d(g[::-1]), np.poly1d(u[::-1]))
    return np.mod(gu.coeffs, 2)[::-1]


def div_mod(vector, g):
    q, r = np.polydiv(vector[::-1], g[::-1])
    q = np.mod(q.astype(int), 2)[::-1]
    r = np.mod(r.astype(int), 2)[::-1]
    return q, r


f = generate_f_vector(n)
# g = np.array([1, 0, 0, 0, 1, 0, 1, 1, 1])
g = np.vectorize(int)([i for i in input()])
# u = np.array([0, 1, 1, 0, 1, 1, 0])
u = np.vectorize(int)([i for i in input()])

h = np.mod(np.polydiv(f, g)[0], 2).astype(int)
G = cyclic_matrix(zeroes(g), k, n)
H_ = cyclic_matrix(zeroes(h), n - k, n)
print('g(x):', g)
pretty_print(Polynomial(g))
print('\nh(x):', h)
pretty_print(Polynomial(h))
print(f'\nПорождающая матрица G:\n{G}')
print(f'Промежуточная матрица H:\n{H_}')
print(f'Проверочная матрица H:\n{H_[:, ::-1]}')
encoded = encode(g, u)
print(f'\nЗакодированное сообщение:\n{encoded}')
pretty_print(Polynomial(encoded))

# vector = np.array([0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1])
print()
vector = np.vectorize(int)([i for i in input()])
remainder = div_mod(vector, g)[1]

# print("Частное:", quotient)
print(f'\nS(x)0:\n{remainder}')
pretty_print(Polynomial(remainder))
print()
i = 0
while np.count_nonzero(remainder) > d:
    remainder = np.polymul(np.array([1, 0]), remainder[::-1])[::-1]
    remainder = div_mod(remainder, g)[1]
    if np.count_nonzero(remainder) <= d:
        print('Исправляющий:')
    print(f'S(x){i + 1}')
    print(remainder)
    pretty_print(Polynomial(remainder))
    print()
    i += 1
print('Подходящий номер вектора:', i)

e = np.concatenate((np.zeros(n - i), [1])).astype(int)
e = np.polymul(e[::-1], remainder)
e = np.polydiv(e, f)[1].astype(int)[::-1]
print(f'Вектор ошибки:\n{e}')
pretty_print(Polynomial(e))
