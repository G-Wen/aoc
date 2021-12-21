from collections import defaultdict


def parse_input(input_filename):
    adj = defaultdict(list)

    with open(input_filename) as f:
        for line in f.readlines():
            a, b = line.strip().split('-')
            adj[a].append(b)
            adj[b].append(a)

    return adj


def find_paths(start, end, visited, route):
    if start == end:
        #print(f"{route}")
        return 1

    paths = [x for x in adj[start] if x not in visited]
    if not paths:
        return 0

    num_paths = 0
    for path in paths:
        if path.islower():
            num_paths += find_paths(path, end, visited+[path], f"{route},{path}")
        else:
            num_paths += find_paths(path, end, visited, f"{route},{path}")
    return num_paths


def find_paths2(start, end, visited, repeated, route):
    if repeated:
        return find_paths(start, end, visited, route)

    paths = [path for path in adj[start] if path != 'start']

    num_paths = 0
    for path in paths:
        if path == end:
            num_paths += 1
            #print(f"{route},{path}")
            continue
        if path.islower():
            if path in visited:
                num_paths += find_paths2(path, end, visited, True, f"{route},{path}")
            else:
                num_paths += find_paths2(path, end, visited+[path], False, f"{route},{path}")
        else:
            num_paths += find_paths2(path, end, visited, repeated, f"{route},{path}")

    return num_paths


adj = parse_input('12input')
print(find_paths('start', 'end', ['start'], "start"))
print(find_paths2('start', 'end', ['start'], False, "start"))

