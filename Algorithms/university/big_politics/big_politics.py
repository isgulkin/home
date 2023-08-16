import heapq


def big_politics(p: list) -> int:
    heapq.heapify(p)
    total = 0
    while len(p) > 1:
        min_1 = heapq.heappop(p)
        min_2 = heapq.heappop(p)
        min_0 = min_1 + min_2
        total += min_0
        heapq.heappush(p, min_0)
    return total
