import math


def distance(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def closest_pair_of_points(points):
    x = sorted(points, key=lambda points: points[0])

    if len(x) <= 3:
        length = 999999999999999
        first = ()
        second = ()
        for i in range(len(x) - 1):
            for j in range(i + 1, len(x)):
                if distance(x[i], x[j]) < length:
                    length = distance(x[i], x[j])
                    first = x[i]
                    second = x[j]
        return length, first, second
    else:
        right = x[len(x) // 2:]
        left = x[:len(x) // 2]
        right_length, right_first, right_second = closest_pair_of_points(right)
        left_length, left_first, left_second = closest_pair_of_points(left)
        if right_length < left_length:
            length = right_length
            first = right_first
            second = right_second
        else:
            length = left_length
            first = left_first
            second = left_second
        middle = left[len(left) - 1][0]
        tape = []
        for i in x:
            if ((middle - length) < i[0]) and (i[0] < (middle + length)):
                tape += [i]
            elif i[0] > middle + length:
                break
        y = sorted(tape, key=lambda points: points[1])
        for i in range(len(y) - 1):
            c = min(len(y), i + 8)
            for j in range(i + 1, c):
                if distance(y[i], y[j]) < length:
                    length = distance(y[i], y[j])
                    first = y[i]
                    second = y[j]
        return length, first, second
