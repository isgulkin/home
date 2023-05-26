def encode(s):
    if s == '':
        return ''
    encoded_str = ''
    current_char = s[0]
    count = 1

    for i in range(1, len(s)):
        if s[i] == current_char:
            count += 1
        else:
            if count == 1:
                encoded_str += current_char
            else:
                encoded_str += str(count) + current_char
                count = 1

            current_char = s[i]

    if count == 1:
        encoded_str += current_char
    else:
        encoded_str += str(count) + current_char

    return encoded_str


def decode(st):
    decoded_str = ''
    count_str = ''
    for char in st:
        if char.isdigit():
            count_str += char
        else:
            if count_str:
                count = int(count_str)
                decoded_str += char * count
                count_str = ''
            else:
                decoded_str += char

    return decoded_str
