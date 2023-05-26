def convert(x):
    """
    В возврящаемую строку дописываются:
    :param Pling: если число number делится на 3,
    :param Plang: если число number делится на 5,
    :param Plong: если число number делится на 7,
    само число number, если оно не делится ни на 3, ни на 5, ни на 7.
    """
    y = ""
    if x % 3 == 0:
        y += "Pling"
    if x % 5 == 0:
        y += "Plang"
    if x % 7 == 0:
        y += "Plong"
    if y == "":
        return str(x)
    else:
        return y
