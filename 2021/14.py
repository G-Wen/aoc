from collections import defaultdict


def parse_input(input_filename):
    with open(input_filename) as f:
        polymer = f.readline().strip()
        pair_dict = defaultdict(int)
        for i in range(len(polymer) - 1):
            pair_dict[polymer[i:i+2]] += 1
        f.readline()
        rules = dict()
        for line in f:
            start, end = line.strip().split(' -> ')
            rules[start] = (start[0]+end, end+start[1])
        return pair_dict, rules, polymer[-1]


def step(pair_dict, rules):
    post_insertion_dict = defaultdict(int)
    for pair in pair_dict:
        if pair in rules:
            post_insertion_dict[rules[pair][0]] += pair_dict[pair]
            post_insertion_dict[rules[pair][1]] += pair_dict[pair]
        else:
            post_insertion_dict[pair] += pair_dict[pair]
    return post_insertion_dict


def polymer_insertion(pair_dict, rules, steps):
    for _ in range(steps):
        pair_dict = step(pair_dict, rules)
    return pair_dict


def diff_calc(pair_dict, last_char):
    counter = defaultdict(int)
    for pair in pair_dict:
        counter[pair[0]] += pair_dict[pair]
    counter[last_char] += 1
    counter = sorted(counter.values())
    return counter[-1] - counter[0]


pair_dict, rules, last_char = parse_input('14input')

# Part 1
pair_dict = polymer_insertion(pair_dict, rules, 10)
print(diff_calc(pair_dict, last_char))

# Part 2
pair_dict = polymer_insertion(pair_dict, rules, 30)
print(diff_calc(pair_dict, last_char))

