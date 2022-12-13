from itertools import accumulate, product
from collections import defaultdict
import math

def parse_input(input_filename):
    with open(input_filename) as f:
        pass

    return 0

def cumsum(x):
    return list(enumerate(accumulate(i for i in range(x, 0, -1)), 1))

def stopping_speed(x, lower, upper):
    return lower <= sum(range(x+1)) <= upper

def get_possible_xs(min_x, max_x):
    steps = defaultdict(list)
    min_speed = math.ceil((math.sqrt(1+8*min_x) - 1) / 2)-1
    max_speed = max_x

    for speed in range(min_speed, max_speed+1):
        if stopping_speed(speed, min_x, max_x):
            steps[0].append(speed)
        positions = list(filter(lambda x: min_x <= x[1] <= max_x, cumsum(speed)))
        for step, pos in positions:
            steps[step].append(speed)

    return steps

def get_possible_ys(min_y, max_y, max_steps):
    steps = defaultdict(list)
    max_init_speed = math.floor((max_steps-1)/2)  # assuming max_y is negative
    print(f"Max init speed which doesn't stay in: {max_init_speed}")
    # calculate all initial speeds for initial x velocites that do not stay within the target range
    for init_speed in range(max_init_speed, min_y-1, -1):
        y_speeds = [init_speed - i for i in range(max_steps)]
        positions = list(enumerate(accumulate(y_speeds), 1))
        filtered = list(filter(lambda x: min_y <= x[1] <= max_y, positions))
        for step, pos in filtered:
            steps[step].append(init_speed)

    # calculate all possible initial velocites
    return steps


def calculate_all_possible_trajectories(target_min_x, target_max_x, target_min_y, target_max_y):
    possible_xs = get_possible_xs(target_min_x, target_max_x)
    max_steps = max(possible_xs.keys())
    possible_ys = get_possible_ys(target_min_y, target_max_y, max_steps)
    max_init_y = float('-inf')
    for speeds in possible_ys.values():
        max_init_y = max(max_init_y, max(speeds))
    print(f"Maximum initial y velocity: {max_init_y}, resulting in max height of {(max_init_y**2+max_init_y)/2}")

    possible_steps = set(possible_ys.keys()) & set(possible_ys.keys())
    print(possible_steps)
    print(possible_xs[0])

    init_velos = defaultdict(list)
    for step in possible_steps:
        init_velos[step].extend(product(possible_xs[step], possible_ys[step]))
    print(init_velos[22])
    print(init_velos[23])



target_min_x, target_max_x, target_min_y, target_max_y = 248, 285, -85, -56
#calculate_all_possible_trajectories(target_min_x, target_max_x, target_min_y, target_max_y)

velos = set()
for x in range(22, 285+1):
    for y in range(-85, 84+1):
        x_speeds = [max(x-i, 0) for i in range(170)]
        y_speeds = [y-i for i in range(179)]
        x_traj = accumulate(x_speeds)
        y_traj = accumulate(y_speeds)
        trajectory = list(zip(x_traj, y_traj))
        filtered = list(filter(lambda pos: target_min_x <= pos[0] <= target_max_x and target_min_y <= pos[1] <= target_max_y, trajectory))
        if filtered:
            velos.add((x, y))
print(len(velos))
# >1919

#print(possible_ys)
#possible_xs = get_possible_xs(248, 285)
#possible_ys = get_possible_ys(-85, -56, 23)

print((84**2+84)/2)