def parse_input(input_filename):
    with open(input_filename) as f:
        return [int(h) for h in f.readlines()]


def part1(heights):
    current_height = heights[0]
    count = 0
    for height in heights[1:]:
        if height > current_height:
            count += 1
        current_height = height
    print(f"# of increases: {count}")
    return count


def part2(heights):
    count = 0
    for i in range(3, len(heights)):
        if heights[i] > heights[i-3]:
            count += 1
    print(f"# of increasing windows: {count}")
    return count


heights = parse_input('1input')
part1(heights)
part2(heights)
