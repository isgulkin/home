from typing import List


def sums(s: List[int]) -> int:
    if len(s) == 0:
        return 0
    uniq_sum = {0}
    for x in s:
        tmp_uniq_sum = set()
        for p in uniq_sum:
            tmp_uniq_sum.add(p + x)
        uniq_sum |= tmp_uniq_sum
    return len(uniq_sum)
