import galois
import numpy as np
from galois import Array, Poly


def evaluate_polynomial(polynomial: galois.Poly,
                        field_elements: list) -> list[Array | Poly]:
    polynomial_values = []
    for element in field_elements:
        polynomial_value = polynomial(element)
        polynomial_degrees = polynomial.degrees
        polynomial_terms = []

        for i, coefficient in enumerate(polynomial.coefficients()):
            polynomial_terms.append(coefficient * element ** polynomial_degrees[i])

        print('a(' + str(element) + ') =',
              ' + '.join(map(str, polynomial_terms)), '=', end=' ')

        print(*['[' + power_to_int[i.__str__()] + ']'
                for i in polynomial_terms], sep=" + ", end=" = " + str(polynomial_value) + "\n")
        polynomial_values.append(polynomial_value)

    return polynomial_values


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

        print('S(' + str(element) + ") = v'(" + str(element) + ") =",
              ' + '.join(map(str, polynomial_terms)), '=', polynomial_value, end=' ')

        print(*['[' + power_to_int.get(i.__str__(), '0') + ']'
                for i in polynomial_terms], sep=" + ", end=" = " + str(polynomial_value) + "\n")

        polynomial_values.append(polynomial_value)
        if polynomial_value == 0:
            break
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


prime, power = 3, 2
GaloisField = galois.GF(prime ** power, irreducible_poly='x^2+x+2', repr='power')

power_reprs = [i.__str__() for i in GaloisField.elements][1:]

int_reprs = [np.base_repr(i, prime).zfill(power) for i in GaloisField.elements][1:]

power_to_int, int_to_power = {}, {}
for i in range(len(power_reprs)):
    power_to_int[power_reprs[i]] = int_reprs[i]
    int_to_power[int_reprs[i]] = power_reprs[i]

power_to_int = dict(sorted(power_to_int.items()))
for key, value in power_to_int.items():
    print(str(key) + ' = [' + str(value) + ']')

elements = sorted(GaloisField.elements, key=lambda x: x.__str__())

print('--------------------------------------------------------------------')

print('Нахождение вектора u путём подставления в а(х) всех элементов поля\n')

q, w = GaloisField.Vector([1, 0]), GaloisField.Vector([2, 1])
a = [1, 1, q, w][::-1]
a = galois.Poly(a, field=GaloisField)
u = evaluate_polynomial(a, elements[1:])
print('\nВектор u:', *u)

a_5, a_7 = GaloisField.Vector([2, 0]), GaloisField.Vector([1, 1])
v_ = [0, 0, 0, 0, a_5, 0, a_7, 1][::-1]
v_ = galois.Poly(v_, field=GaloisField)

print("Представление v' в виде полинома: v'(x) =", v_)

print('--------------------------------------------------------------------')

print('Нахождение S(x)\n')
sz = find_sx(v_, elements[2:])
sz = sz[:len(sz) - 1]
sz = galois.Poly(sz[::-1], field=GaloisField)
print('\nПредставление S(z) в виде полинома: S(z) =', str(sz).replace('x', 'z'))

print('--------------------------------------------------------------------')

q = galois.Poly([1, 0, 0, 0, 0], field=GaloisField)
q_0 = divmod(q, sz)[0]
print('Частное получившееся от деления двух многочленов:')
print('q_0 = (' + str(q).replace('x', 'z') + ') / [' + str(sz).replace('x', 'z') + '] = ' + str(q_0).replace('x', 'z'))

free_term = q_0.coeffs[-1]
print('Свободный член: q_0 =', free_term)

print('--------------------------------------------------------------------')

gamma = free_term ** -1
print('Нахождение γ:\n' + 'γ * ' + str(free_term) + ' = 1, тогда γ =', gamma)

sigma = gamma * q_0
print('Нахождение σ:\nσ(z) = γ * q_0(z) = [' + str(gamma).replace('x', 'z') + '] * ', end='')
print('[' + str(q_0).replace('x', 'z') + '] =', str(sigma).replace('x', 'z'))

print('--------------------------------------------------------------------')

print('Теперь найдём корни уравнения: ' + str(sigma).replace('x', 'z') + ' = 0\n')

inverse_elements = find_errors(sigma, elements[1:])
print('\nВектор ошибок(ещё надо найти обратные элементы):', *inverse_elements)

error_vector = [element ** -1 for element in inverse_elements]
print('Вектор ошибок, в котором степени элементов α -- места ошибок:', *error_vector)
