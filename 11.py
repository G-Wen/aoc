import itertools


def parse_input(input_filename):
    octopodes = {}
    with open(input_filename) as f:
        for y, line in enumerate(f.readlines()):
            line = line.strip()
            for x, energy in enumerate(line):
                octopodes[(x, y)] = int(energy)
    return octopodes, x+1, y+1


def display(octopodes, width, height):
    for y in range(width):
        line = ""
        for x in range(height):
            line += str(octopodes[(x, y)])
        print(line)
    print("\n")


def get_adj(x, y):
    adjs = []
    for dx, dy in itertools.product([-1, 0, 1], repeat=2):
        if dx or dy:
            adjs.append((x+dx, y+dy))
    return adjs


def step(octopodes):
    flashed = set()

    to_flash = []
    for x in octopodes:
        octopodes[x] += 1
        if octopodes[x] == 10:
            to_flash.append(x)

    while to_flash:
        octopus = to_flash.pop(0)
        flashed.add(octopus)
        adjs = get_adj(*octopus)
        for adj in adjs:
            if adj in octopodes:
                octopodes[adj] += 1
                if octopodes[adj] >= 10:
                    if adj not in to_flash and adj not in flashed:
                        to_flash.append(adj)

    for octopus in flashed:
        octopodes[octopus] = 0

    return octopodes, len(flashed)


octopodes, width, height = parse_input('11input')
total_flashes = 0
for i in range(100):
    octopodes, num_flahes = step(octopodes)
    total_flashes += num_flahes
    # display(octopodes, width, height)
print(f"Total flashes after 100 steps: {total_flashes}")


octopodes, width, height = parse_input('11input')
step_count = 0
while True:
    octopodes, num_flahes = step(octopodes)
    step_count += 1
    if num_flahes == width*height:
        break
print(f"First step where all octopodes flash: {step_count}")
