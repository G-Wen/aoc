import collections
import itertools

class Scanner:
    def __init__(self, scanner_id, beacons):
        self.id = scanner_id
        self.beacons = beacons
        self.beacon2hash = {beacon: knn_hash(beacon, beacons, 2) for beacon in beacons}
        self.hash2beacon = {v: k for k, v in self.beacon2hash.items()}

    def rotate_and_shift(self, rotation, shift=(0,0,0)):
        self.beacons = [apply_rotation(b, rotation) for b in self.beacons]
        self.beacons = [(b[0]+shift[0], b[1]+shift[1], b[2]+shift[2]) for b in self.beacons]
        self.beacon2hash = {beacon: knn_hash(beacon, self.beacons, 2) for beacon in self.beacons}
        self.hash2beacon = {v: k for k, v in self.beacon2hash.items()}

    def merge(self, other_scanner):
        self.beacons.extend(other_scanner.beacons)
        self.beacons = list(set(self.beacons))
        self.beacon2hash = {beacon: knn_hash(beacon, self.beacons, 2) for beacon in self.beacons}
        self.hash2beacon = {v: k for k, v in self.beacon2hash.items()}


def parse_input(input_filename):
    scanners = {}
    beacons = []
    with open(input_filename) as f:
        for line in f:
            line = line.strip()
            if not line:
                scanners[scanner_id] = Scanner(scanner_id, beacons)
                beacons = []
            else:
                if line.startswith("---"):
                    scanner_id = line.split()[2]
                    pass
                else:
                    beacons.append(tuple(int(coord) for coord in line.split(",")))
    scanners[scanner_id] = (Scanner(scanner_id, beacons))
    return scanners


def rotate(coord, axis, times):
    if not times:
        return coord

    for time in range(times):
        if axis == 0:
            coord = (coord[0], -coord[2], coord[1])
        if axis == 1:
            coord = (-coord[2], coord[1], coord[0])
        if axis == 2:
            coord = (-coord[1], coord[0], coord[2])

    return coord


def apply_rotation(coord, rot_id, about=None):
    if not rot_id:
        return coord

    primary_times = rot_id // 4
    secondary_times = rot_id % 4

    if about:
        coord = (coord[0] - about[0], coord[1] - about[1], coord[2] - about[2])

    if primary_times < 4:
        coord = rotate(coord, 0, secondary_times)
        coord = rotate(coord, 1, primary_times)
    elif primary_times == 4:
        coord = rotate(coord, 0, secondary_times)
        coord = rotate(coord, 2, 1)
    else:
        coord = rotate(coord, 0, secondary_times)
        coord = rotate(coord, 2, 3)

    if about:
        coord = (coord[0] + about[0], coord[1] + about[1], coord[2] + about[2])

    return coord


def knn_hash(beacon, beacons, neighbours):
    x, y, z = beacon
    metrics = [(b[0]-x)**2 + (b[1] - y)**2 + (b[2] - z)**2 for b in beacons]
    metrics.sort()
    if neighbours >= len(metrics):
        neighbours = len(metrics)
    return sum(metrics[:neighbours+1])


def find_potential_merges(scanners):
    candidates = []
    for id1, id2 in itertools.combinations(scanners, 2):
        scanner1, scanner2 = scanners[id1], scanners[id2]
        counter = collections.Counter()
        for scanner in [scanner1, scanner2]:
            counter.update(scanner.beacon2hash.values())
            most_common = counter.most_common(5)
            if most_common[-1][-1] == 2:
                candidates.append(((scanner1.id, scanner2.id), [x for x in counter if counter[x] == 2]))
    return candidates


def check_match(candidates, hashes, scanners):
    id1, id2 = candidates
    scanners = scanners[id1], scanners[id2]
    points = [[scan.hash2beacon[hash] for hash in hashes] for scan in scanners]
    rel_diffs = [[(p[0]-sp[0][0], p[1]-sp[0][1], p[2]-sp[0][2]) for p in sp] for sp in points]

    match, rotation, shift= False, None, None
    for rot in range(24):
        rotated_diffs = [apply_rotation(coord, rot) for coord in rel_diffs[1]]
        if rotated_diffs == rel_diffs[0]:
            rotated_points = [apply_rotation(coord, rot) for coord in points[1]]
            match = True
            rotation = rot
            shift = (points[0][0][0] - rotated_points[0][0], points[0][0][1] - rotated_points[0][1], points[0][0][2] - rotated_points[0][2])
            #print(f"{id1} and {id2} match with rotation {rot}, and shift by {shift}")
            break

    return match, rotation, shift


def furthest_beacon_pair(locations):
    max_dist = float('-inf')
    for p1, p2 in itertools.combinations(locations, 2):
        max_dist = max(max_dist, sum(abs(p1[i] - p2[i]) for i in range(3)))
    return max_dist


scanners = parse_input('19input')
cannonical_distances = {'0': (0, 0, 0)}
relative_distances = {}

# Get all the positions of the beacons relative to the first scanner
while len(scanners) > 1:
    candidates_info = find_potential_merges(scanners)
    merged = []
    for candidates, hashes in candidates_info:
        merger, mergee = candidates
        if merger in merged or mergee in merged:
            continue
        match, rotation, shift = check_match(candidates, hashes, scanners)
        if match:
            merger_scanner = scanners[merger]
            mergee_scanner = scanners[mergee]
            mergee_scanner.rotate_and_shift(rotation, shift=shift)
            merger_scanner.merge(mergee_scanner)
            del scanners[mergee]
            merged.append(mergee)
            if merger in cannonical_distances:
                cannonical_distances[mergee] = tuple(cannonical_distances[merger][i] + shift[i] for i in range(3))
            else:
                relative_distances[(merger, mergee)] = shift

cannonical_scanner = scanners['0']
print(f"Number of unique beacons: {len(cannonical_scanner.beacons)}")

# Get all the positions of the scanners relative to the first scanner
while relative_distances:
    for key in list(relative_distances.keys()):
        if key[0] in cannonical_distances:
            cannonical_distances[key[1]] = tuple(cannonical_distances[key[0]][i] - relative_distances[key][i] for i in range(3))
        del relative_distances[key]

print(f"Furthest Manhatten distance between beacons: {furthest_beacon_pair(cannonical_distances.values())}")

