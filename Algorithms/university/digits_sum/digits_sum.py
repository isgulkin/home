from typing import List
from random import randint


def quicksort(arr: List[int]) -> list[int] | int:
    if len(arr) < 2:
        return arr
    lower, equal, higher = [], [], []
    p = arr[randint(0, len(arr) - 1)]
    for item in arr:
        if item < p:
            lower.append(item)
        elif item == p:
            equal.append(item)
        else:
            higher.append(item)
    return quicksort(lower) + equal + quicksort(higher)


def min_digits_sum(arr: List[int]) -> int:
    arr = quicksort(arr)
    first_digit_sum, second_digit_sum = 0, 0
    for i in range(len(arr)):
        if i % 2 == 0:
            first_digit_sum = first_digit_sum * 10 + arr[i]
        else:
            second_digit_sum = second_digit_sum * 10 + arr[i]
    return first_digit_sum + second_digit_sum
