import galois
import numpy as np

from galois import Array, Poly


def find_sx(polynomial: galois.Poly,
            field_elements: list) -> list[Array | Poly]:
    polynomial_values = []
    for element in field_elements:
        polynomial_value = polynomial(element)
        polynomial_degrees = polynomial.degrees
        polynomial_terms = []

        for i, coefficient in enumerate(polynomial.coefficients()):
            if coefficient != 0:
                polynomial_terms.append(coefficient * element ** polynomial_degrees[i])

        print('S(' + str(element) + ") = v(" + str(element) + ") =",
              ' + '.join(map(str, polynomial_terms)), '=', polynomial_value, end=' ')

        print(*['[' + power_to_int.get(i.__str__(), '0') + ']'
                for i in polynomial_terms], sep=" + ", end=" = " + str(polynomial_value) + "\n")

        polynomial_values.append(polynomial_value)
    return polynomial_values


def find_errors(polynomial: galois.Poly,
                field_elements: list) -> list[Array | Poly]:
    polynomial_values = []
    for element in field_elements:
        polynomial_value = polynomial(element)
        polynomial_degrees = polynomial.degrees
        polynomial_terms = []

        for i, coefficient in enumerate(polynomial.coefficients()):
            if coefficient != 0:
                polynomial_terms.append(coefficient * element ** polynomial_degrees[i])

        print('σ(' + str(element) + ") =",
              ' + '.join(map(str, polynomial_terms)), '=', end=' ')

        print(*['[' + power_to_int.get(i.__str__(), '0') + ']'
                for i in polynomial_terms], sep=" + ", end=" = " + str(polynomial_value) + "\n")

        if polynomial_value == 0:
            polynomial_values.append(element)
    return polynomial_values


def convert_str_to_npvec(s):
    return np.array(list(map(int, s)))


def convert_npvec_to_str(v):
    return ''.join(map(str, v))


def foo(ob):
    return convert_npvec_to_str(GaloisField(ob.vector()))


p, m, t = 2, 3, 3

GaloisField = galois.GF(p ** m, irreducible_poly='x^3+x^2+1', repr='power')

power_reprs = [i.__str__() for i in GaloisField.elements][1:]

int_reprs = [np.base_repr(i, p).zfill(m) for i in GaloisField.elements][1:]

power_to_int, int_to_power = {}, {}
for i in range(len(power_reprs)):
    power_to_int[power_reprs[i]] = int_reprs[i]
    int_to_power[int_reprs[i]] = power_reprs[i]

elements = sorted(GaloisField.elements, key=lambda x: x.__str__())

v_ = galois.Poly([1, 1, 1], field=GaloisField)

print('--------------------------------------------------------------------')

print('Найдём все S(x)\n')

GaloisField.repr('power')
Sx = find_sx(v_, elements[1:])

print('--------------------------------------------------------------------')

matrix = np.array([[1, 0, 0],
                   [Sx[2], Sx[1], 1],
                   [Sx[4], Sx[3], Sx[2]]])

print('Получившаяся матрица\n\n', GaloisField(matrix))

print('--------------------------------------------------------------------')

print('Решения матричного уравнения')

matrix_x = np.array([Sx[1], Sx[3], Sx[5]])
x = np.linalg.solve(GaloisField(matrix), GaloisField(matrix_x))

for i in range(len(x)):
    print(f'σ{i + 1} = ', x[i])

sigma = galois.Poly([*reversed(x), 1], field=GaloisField)

print('Многочлен локаторов ошибок: σ(x) =', str(sigma).replace('x', 'z'))

print('--------------------------------------------------------------------')

print('Нахождение вектора ошибок подставлением в σ(x) всех элементов, там где σ(x) = 0, решение - элемент обратный x\n')

inverse_elements = find_errors(sigma, elements[1:])

print('--------------------------------------------------------------------')

print('\nВектор ошибок(ещё надо найти обратные элементы):', *inverse_elements)

error_vector = [element ** -1 for element in inverse_elements]
print('Вектор ошибок, в котором степени элементов α -- места ошибок:', *error_vector)


