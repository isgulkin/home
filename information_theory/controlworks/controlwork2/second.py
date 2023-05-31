import galois
import numpy as np

from galois import Array, Poly


def evaluate_polynomial(polynomial: galois.Poly,
                        field_elements: galois.FieldArray) -> list[Array | Poly]:
    polynomial_values = []
    for element in field_elements:
        polynomial_value = polynomial(element)
        polynomial_degrees = polynomial.degrees
        polynomial_terms = []

        for i, coefficient in enumerate(polynomial.coefficients()):
            polynomial_terms.append(coefficient * element ** polynomial_degrees[i])

        print('a(' + str(element) + ') =',
              ' + '.join(map(str, polynomial_terms)), '=', end=' ')

        print(*['[' + gstr_v[i.__str__()] + ']'
                for i in polynomial_terms], sep=" + ", end=" = " + str(polynomial_value) + "\n")
        polynomial_values.append(polynomial_value)

    return polynomial_values


def find_sx(polynomial: galois.Poly,
            field_elements: galois.FieldArray) -> list[Array | Poly]:
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

        print(*['[' + gstr_v.get(i.__str__(), '0') + ']'
                for i in polynomial_terms], sep=" + ", end=" = " + str(polynomial_value) + "\n")

        polynomial_values.append(polynomial_value)
        if polynomial_value == 0:
            break
    return polynomial_values


def find_errors(polynomial: galois.Poly,
                field_elements: galois.FieldArray) -> list[Array | Poly]:
    polynomial_values = []
    for element in field_elements:
        polynomial_value = polynomial(element)
        polynomial_degrees = polynomial.degrees
        polynomial_terms = []

        for i, coefficient in enumerate(polynomial.coefficients()):
            if coefficient != 0:
                polynomial_terms.append(coefficient * element ** polynomial_degrees[i])

        print('sigma(' + str(element) + ") =",
              ' + '.join(map(str, polynomial_terms)), '=', end=' ')

        print(*['[' + gstr_v.get(i.__str__(), '0') + ']'
                for i in polynomial_terms], sep=" + ", end=" = " + str(polynomial_value) + "\n")

        if polynomial_value == 0:
            polynomial_values.append(element)
    return polynomial_values


p, m = 3, 2
GF = galois.GF(p ** m, irreducible_poly='x^2+x+2', repr='power')

gstrs = [i.__str__() for i in GF.elements][1:]

GF.repr('int')
els = [np.base_repr(i, p).zfill(m) for i in GF.elements][1:]
gstr_v, v_gstr = {}, {}
for i in range(len(gstrs)):
    gstr_v[gstrs[i]] = els[i]
    v_gstr[els[i]] = gstrs[i]
GF.repr('power')

elements = sorted(GF.elements, key=lambda x: x.__str__())
print('--------------------------------------------------------------------')
print('Нахождение вектора u путём подставления в а(х) всех элеметов поля\n')

q, w = GF.Vector([1, 0]), GF.Vector([2, 1])
a = [1, 1, q, w][::-1]
a = galois.Poly(a, field=GF)
u = evaluate_polynomial(a, elements[1:])
print('\nВектор u:', *u)
a_5, a_7 = GF.Vector([2, 0]), GF.Vector([1, 1])
v_ = [0, 0, 0, 0, a_5, 0, a_7, 1][::-1]
v_ = galois.Poly(v_, field=GF)
print("Представление v' в виде полинома: v'(x) =", v_)
print('--------------------------------------------------------------------')
print('Нахождение S(x)\n')

sz = find_sx(v_, elements[2:])
sz = sz[:len(sz) - 1]

sz = galois.Poly(sz[::-1], field=GF)
print('\nПредставление S(z) в виде полинома: S(z) =', str(sz).replace('x', 'z'))
print('--------------------------------------------------------------------')
q = galois.Poly([1, 0, 0, 0, 0], field=GF)
q_0 = divmod(q, sz)[0]

print('Частное получившееся от деления двух многочленов:')
print('q_0 = (' + str(q).replace('x', 'z') + ') / [' + str(sz).replace('x', 'z') + '] = ' + str(q_0).replace('x', 'z'))
free_term = q_0.coeffs[-1]
print('Свободный член: q_0 =', free_term)

print('--------------------------------------------------------------------')

gamma = free_term ** -1
print('Нахождение gamma:\n' + 'gamma * ' + str(free_term) + ' = 1, тогда gamma =', gamma)
print('Пометка для Стёпы, gamma похожа на y')

sigma = gamma * q_0
print('Нахождение sigma:\nsigma(z) = gamma * q_0(z) = [' + str(gamma).replace('x', 'z') + '] * ', end='')
print('[' + str(q_0).replace('x','z') + '] =',str(sigma).replace('x', 'z'))

print('--------------------------------------------------------------------')

print('Теперь найдём корни уравнения: ' + str(sigma).replace('x', 'z') + ' = 0\n')

'''
a_5, a_7 = GF.Vector([2, 0]), GF.Vector([1, 1])
v_ = [0, 0, 0, 0, a_5, 0, a_7, 1][::-1]
v_ = galois.Poly(v_, field=GF)
sz = sss(v_, elements[2:])
'''
inverse_elements = find_errors(sigma, elements[1:])
print('\nВектор ошибок(ещё надо найти обратные элементы):', *inverse_elements)
error_vector = [element ** -1 for element in inverse_elements]
print('Вектор ошибок, в котором степени элементов α -- места ошибок:', *error_vector)
