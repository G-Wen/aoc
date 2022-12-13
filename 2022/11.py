def parse_input(input_filename):
    monkeys = []
    with open(input_filename) as f:
        lines = f.readlines()
        lines.append('\n')
        num_monkeys = len(lines)//7
    for i in range(num_monkeys):
        monkey = dict()
        monkey['items'] = [int(x.replace(',', '')) for x in lines[i*7+1].split()[2:]]
        monkey['operation'] = lines[i*7+2].split()[-2:]
        if monkey['operation'] == ['*', 'old']:
            monkey['operation'] = ['**', '2']
        monkey['operation'][1] = int(monkey['operation'][1])
        monkey['test'] = [int(lines[i*7+3].split()[-1]), int(lines[i*7+4].split()[-1]), int(lines[i*7+5].split()[-1])]
        monkey['inspected'] = 0
        monkeys.append(monkey)
    return monkeys

def apply_operation(operation, worry):
    op, quant = operation
    if op == '+':
        return worry + quant
    elif op == '*':
        return worry * quant
    elif op == '**':
        return worry ** quant
    else:
        raise

def throw_test(test, worry):
    if not worry % test[0]:
        return test[1]
    return test[2]

def inspect_and_throw(monkeys, i):
    monkey = monkeys[i]
    for worry in monkey['items']:
        new_worry = apply_operation(monkey['operation'], worry)
        # Part 1:
        # new_worry //= 3
        # Part 2:
        new_worry %= 9699690  # product of the first 8 primes
        monkeys[throw_test(monkey['test'], new_worry)]['items'].append(new_worry)
        monkey['inspected'] += 1
    monkey['items'] = []
    return monkeys

def play_round(monkeys):
    for i in range(len(monkeys)):
        monkeys = inspect_and_throw(monkeys, i)

    for i in []: #range(len(monkeys)):
        print(monkeys[i]['items'])
    return monkeys

def play_rounds(monkeys, n):
    for i in range(n):
        # print(f"Round {i+1}")
        monkeys = play_round(monkeys)

    inspections = []
    for i in range(len(monkeys)):
        print(f"Monkey {i}: {monkeys[i]['inspected']}")
        inspections.append(monkeys[i]['inspected'])
    inspections.sort()
    inspections.reverse()
    print(f"{inspections[0] * inspections[1]}")
    return monkeys, inspections

monkeys = parse_input('11input')

monkeys, inspections = play_rounds(monkeys, 10000)
