def parse_inputfile(input_filename):
    with open(input_filename) as f:
        course = []
        for line in f:
            dir, value = line.split()
            course.append((dir, int(value)))
        return course


def part1():
    xpos, depth = 0, 0
    for dir, value in course:
        if dir == 'forward':
            xpos += value
        elif dir == 'down':
            depth += value
        else:
            depth -= value
    print(f"Part 1: {xpos*depth}")


def part2():
    xpos, depth, aim = 0, 0, 0
    for dir, value in course:
        if dir == 'forward':
            xpos += value
            depth += value*aim
        elif dir == 'down':
            aim += value
        else:
            aim -= value
    print(f"Part 2: {xpos*depth}")


course = parse_inputfile('2input')
part1()
part2()
