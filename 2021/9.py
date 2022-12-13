def parse_input(input_filename):
    map = {}
    with open(input_filename) as f:
        for y, line in enumerate(f.readlines()):
            line = line.strip()
            for x, height in enumerate(line):
                map[(x, y)] = int(height)

    return map


def get_adjs(x, y):
    return [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]


def get_low_points(map):
    low_points = set()
    for tile in map:
        adjacents = [tile for tile in get_adjs(*tile) if tile in map]
        low_point = True
        for adj in adjacents:
            if map[tile] >= map[adj]:
                low_point = False
                break
        if low_point:
            low_points.add(tile)
    return low_points


def map_risk(map):
    risk = 0
    low_points = get_low_points(map)
    for point in low_points:
        risk += map[point] + 1
    return risk


map = parse_input('9inputtest')
risk = map_risk(map)
print(risk)

map = parse_input('9input')
risk = map_risk(map)
print(risk)
