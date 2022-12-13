import heapq
import itertools


def parse_input(input_filename):
    cavern = dict()
    with open(input_filename) as f:
        for y, line in enumerate(f.readlines()):
            line = line.strip()
            for x, risk in enumerate(line):
                cavern[(x, y)] = {'risk': int(risk), 'min_risk': float('inf')}

    return cavern


def get_neighbours(tile):
    return [(tile[0]+dx, tile[1]+dy) for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]]


def min_risk_cavern(cavern):
    cavern[(0, 0)]['min_risk'] = 0
    frontier = []
    heapq.heappush(frontier, (cavern[(0, 0)]['min_risk'], (0, 0)))
    visited = set()

    while frontier:
        current_tile_risk, tile = heapq.heappop(frontier)
        if tile in visited:
            continue
        visited.add(tile)

        neighbours = get_neighbours(tile)
        for neighbour in neighbours:
            if neighbour not in cavern or neighbour in visited:
                continue
            cavern[neighbour]['min_risk'] = min(cavern[neighbour]['min_risk'], current_tile_risk + cavern[neighbour]['risk'])
            heapq.heappush(frontier, (cavern[neighbour]['min_risk'], neighbour))

    return cavern


def expand_cavern(cavern):
    for shiftx, shifty in itertools.product(range(5), repeat=2):
        if not shiftx and not shifty:
            continue

        for x, y in itertools.product(range(100), repeat=2):
            risk = cavern[(x, y)]['risk'] + shiftx + shifty
            if risk >= 10:
                risk -= 9

            cavern[(x+(100*shiftx), y+(100*shifty))] = {'risk': risk, 'min_risk': float('inf')}

    return cavern


cavern = parse_input('15input')

# Part 1
cavern = min_risk_cavern(cavern)
print(cavern[(99, 99)]['min_risk'])

# Part 2
cavern = expand_cavern(cavern)
cavern = min_risk_cavern(cavern)
print(cavern[(499, 499)]['min_risk'])
