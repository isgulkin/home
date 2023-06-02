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
    count = 0
    for element in field_elements:
        if count > 3:
            break
        polynomial_value = polynomial(element)
        polynomial_degrees = polynomial.degrees
        polynomial_terms = []

        for i, coefficient in enumerate(polynomial.coefficients()):
            if coefficient != 0:
                polynomial_terms.append(coefficient * element ** polynomial_degrees[i])

        print('S(' + str(element) + ") = v'(" + str(element) + ") =",
              ' + '.join(map(str, polynomial_terms)), '=', end=' ')

        print(*['[' + power_to_int.get(i.__str__(), '0') + ']'
                for i in polynomial_terms], sep=" + ", end=" = " + str(polynomial_value) + "\n")

        polynomial_values.append(polynomial_value)
        count += 1
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
rs = galois.ReedSolomon(n=8, k=4, field=GaloisField)

print('--------------------------------------------------------------------')

print('Нахождение g(x):')
g = galois.Poly([1], field=GaloisField)

for i in rs.roots:
    el = galois.Poly([1, i], field=GaloisField)
    print(f'({g})', '*', f'({el})', end='= ')
    g *= el
    print(g)

print('--------------------------------------------------------------------')

power_reprs = [i.__str__() for i in GaloisField.elements][:]

int_reprs = [np.base_repr(i, prime).zfill(power) for i in GaloisField.elements][:]

power_to_int, int_to_power = {}, {}
for i in range(len(power_reprs)):
    power_to_int[power_reprs[i]] = int_reprs[i]
    int_to_power[int_reprs[i]] = power_reprs[i]

power_to_int = dict(sorted(power_to_int.items()))
for key, value in power_to_int.items():
    print(str(key) + ' = [' + str(value) + ']')

elements = sorted(GaloisField.elements, key=lambda x: x.__str__())

print('--------------------------------------------------------------------')

print("Введите элементы вектора через пробел (от 1 до 4 элементов):")
print('Есть вектор [1, 1, α, α^2] -> вводить элементы поля в виде: 2,1 1,0 0,1 0,1')
input_a = [list(map(int, i.split(','))) for i in input().split()]

input_a = [GaloisField.Vector(i) for i in input_a]

a = galois.Poly(input_a, field=GaloisField)
print('Представление вектора а в виде полинома: a(x)=', a)

print('--------------------------------------------------------------------')

print('Нахождение вектора u путём подставления в а(х) всех элементов поля\n')
u = evaluate_polynomial(a, elements[1:])
print('\nВектор u:', *u)

print("Введите элементы вектора через пробел (от 1 до 4 элементов):")
print('Есть вектор [0, α^5, α, α^5, α^3, α^5, α^4, 1]')
print('-> вводить элементы поля в виде: 2,0 0,0 1,0 2,0 2,2 2,0 0,2 0,1')
input_v = [list(map(int, i.split(','))) for i in input().split()]

input_v = [GaloisField.Vector(i) for i in input_v]

v_ = galois.Poly(input_v, field=GaloisField)

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
print(q)
coefs = q_0.coefficients()

for i in range(len(coefs)):
    mul = [0 for _ in coefs]
    mul[i] = coefs[i]
    print('\t' * i + '-')
    print('\t' * i + f'{sz * galois.Poly(mul, field=GaloisField)}')
    q -= sz * galois.Poly(mul, field=GaloisField)
    print('\t' * i + '----------------------')
    print('\t' * (i + 1) + f'{q}')

print('Частное получившееся от деления двух многочленов:')
print('q_0 = ' + str(q_0).replace('x', 'z'))

free_term = q_0.coeffs[-1]
print('Свободный член: q =', free_term)

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
