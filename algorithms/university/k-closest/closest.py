def binary_search(arr, target):
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = left + (right - left) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return left


def closest(arr, target, count):
    index = binary_search(arr, target)

    left, right = index - 1, index
    result = []

    while count > 0:
        if left < 0:
            result.append(arr[right])
            right += 1
        elif right >= len(arr):
            result.append(arr[left])
            left -= 1
        else:
            left_diff = abs(arr[left] - target)
            right_diff = abs(arr[right] - target)

            if left_diff <= right_diff:
                result.append(arr[left])
                left -= 1
            else:
                result.append(arr[right])
                right += 1

        count -= 1

    return sorted(result)
