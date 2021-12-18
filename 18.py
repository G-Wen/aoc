def add_pair(left, right):
    return f"[{left},{right}]"


def explode(left, pair, right):
    left_num = pair[0]
    right_num = pair[1]
    left = list(reversed(left))
    for ind in range(len(left)):
        char = left[ind]
        if char not in "[,]":
            left[ind] = str(int(left[ind]) + left_num)
            break
    left = list(reversed(left))

    for ind in range(len(right)):
        char = right[ind]
        if char not in "[,]":
            right[ind] = str(int(right[ind]) + right_num)
            break

    return "".join(left) + "0" + "".join(right)


def split_snailfish(string):
    # read until , or ]:
    parsed = []

    while string:
        char, string = string[0], string[1:]
        if char in "[,]":
            parsed.append(char)
        else:
            end_of_int = 0
            for i, c in enumerate(string):
                if c not in ",]":
                    end_of_int = i
            char, string = char + string[:end_of_int], string[end_of_int:]
            num = int(char)
            if num >= 10:
                left = num // 2
                right = num // 2 + (0 if num%2 == 0 else 1)
                parsed.append(f"[{left},{right}]")
                return "".join(parsed)
    return "".join(parsed)


def explode_snailfish(string):
    parsed = []
    depth = 0
    while string:
        char, string = string[0], string[1:]
        if char == '[':
            parsed.append(char)
            depth += 1
        elif char == ',':
            parsed.append(char)
        elif char == ']':
            # if we're at depth >= 5 and we just processed a simple pair, explode
            if depth >= 5 and parsed[-4] == '[':
                pair = [parsed[-3], parsed[-1]]
                string = explode(parsed[:-4], pair, list(string))
                return string
            parsed.append(char)
            depth -= 1
    return "".join(str(x) for x in parsed)


def reduce_snailfish(string):
    # repeat reduce until no change then repeat split until no change
    new_string = explode_snailfish(string)
    while new_string != string:
        string = new_string
        new_string = explode_snailfish(string)

    new_string = split_snailfish(string)
    while new_string != string:
        string = new_string
        new_string = split_snailfish(string)


x = explode(list("[[[["), [9,8], list(",1],2],3],4]"))
y = explode(list("[7,[6,[5,[4,"), [3,2], list("]]]]"))


print(x)
print(y)
