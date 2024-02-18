def message(s: str) -> int:
    s = list(map(int, s))
    if len(s) == 0:
        return 0
    p = 1
    p_prev = 1
    x_prev = s[0]
    for x in s[1:]:
        p_prev, p = p, p + p_prev * (10 <= x_prev * 10 + x <= 33)
        x_prev = x
    return p