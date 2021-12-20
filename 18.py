from functools import reduce
from itertools import combinations


def parse_input(input_filename):
    with open(input_filename) as f:
        snailfish_numbers = [number.strip() for number in f]
    return snailfish_numbers


def read_int(string):
    end_of_int = 0
    for i, c in enumerate(string):
        if c in ",]":
            break
        end_of_int += 1
    return int(string[:end_of_int]), string[end_of_int:]


def explode(left, pair, right):
    left_num = pair[0]
    right_num = pair[1]
    if right_num == 7:
        x = 0
        pass

    left.reverse()
    for ind in range(len(left)):
        char = left[ind]
        if char not in "[,]":
            left[ind] = str(int(left[ind]) + left_num)
            break
    left.reverse()
    left.append("0")

    while right:
        char, right = right[0], right[1:]
        if char in "[,]":
            left.append(char)
        else:
            num, rstring = read_int(char + right)
            num += right_num
            left.append(str(num))
            left.append(rstring)
            break

    return "".join(left)


def split_snailfish(string):
    parsed = []
    while string:
        char, string = string[0], string[1:]
        if char in "[,]":
            parsed.append(char)
        else:
            num, string = read_int(char+string)
            if num >= 10:
                left = num // 2
                right = num // 2 + (0 if num % 2 == 0 else 1)
                parsed.append(f"[{left},{right}]")
                parsed.append(string)
                return "".join(parsed)
            else:
                parsed.append(str(num))
    return "".join(parsed)


def explode_snailfish(string):
    parsed = []
    depth = 0
    while string:
        char, string = string[0], string[1:]
        if char == '[':
            depth += 1
            parsed.append(char)
        elif char == ']':
            # if we're at depth >= 5 and we just processed a simple pair, explode
            if depth >= 5 and parsed[-4] == '[':
                pair = int(parsed[-3]), int(parsed[-1])
                string = explode(parsed[:-4], pair, string)
                return string
            depth -= 1
            parsed.append(char)
        elif char == ',':
            parsed.append(char)
        else:
            num, string = read_int(char + string)
            parsed.append(str(num))
    return "".join(str(x) for x in parsed)


def reduce_snailfish(string):
    while True:
        after_explode = explode_snailfish(string)
        if after_explode != string:
            string = after_explode
            continue
        after_split = split_snailfish(string)
        if after_split != after_explode:
            string = after_split
            continue
        break
    return after_split


def add_snailfish(left, right):
    return reduce_snailfish(f"[{left},{right}]")


def get_parts(snailfish_number):
    depth = 0
    left = []
    while snailfish_number:
        char, snailfish_number = snailfish_number[0], snailfish_number[1:]
        if char == "," and not depth:
            return "".join(left), snailfish_number
        elif char == '[':
            depth += 1
        elif char == ']':
            depth -= 1
        left.append(char)


class SnailfishTree:
    def __init__(self, snailfish_number):
        if snailfish_number[0] != '[':
            self.left = None
            self.right = None
            self.magnitude = int(snailfish_number)
        else:
            left, right = get_parts(snailfish_number[1:-1])
            self.left = SnailfishTree(left)
            self.right = SnailfishTree(right)
            self.magnitude = 3*self.left.magnitude + 2* self.right.magnitude


def snailfish_magnitude(snailfish_number):
    return SnailfishTree(snailfish_number).magnitude


def part1(snailfish_numbers):
    return SnailfishTree(reduce(lambda a, b: add_snailfish(a, b), snailfish_numbers)).magnitude


def part2(snailfish_numbers):
    max_magnitude = float('-inf')
    for x, y in combinations(snailfish_numbers, 2):
        max_magnitude = max(max_magnitude, SnailfishTree(add_snailfish(x, y)).magnitude)
    return max_magnitude


snailfish_numbers = parse_input('18input')
print(part1(snailfish_numbers))
print(part2(snailfish_numbers))



