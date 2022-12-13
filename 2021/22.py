def parse_input(input_filename):
    xmin = xmax = 0
    ymin = ymax = 0
    zmin = zmax = 0
    with open(input_filename) as f:
        instructions = []
        for line in f.readlines():
            line = line.strip()
            inst, zone = line.split()
            x, y, z = zone.split(',')
            x = [int(a) for a in x[2:].split('..')]
            y = [int(a) for a in y[2:].split('..')]
            z = [int(a) for a in z[2:].split('..')]
            xmin = min(xmin, x[0])
            xmax = min(xmax, x[1])

            ymin = min(ymin, y[0])
            ymax = max(ymax, y[1])

            zmin = min(zmin, z[0])
            zmax = max(zmax, z[1])
            instructions.append((inst, x, y, z))

    return instructions, xmin, xmax, ymin, ymax, zmin, zmax


def clamp(range, lower, upper):
    if range[0] > upper or range[1] < lower:
        return 0, -1
    return max(range[0], lower), min(range[1], upper)



def count_lights(instructions):
    on_lights = {}
    for instruction in instructions:
        inst, x, y, z = instruction
        """
        x = clamp(x, -50, 50)
        y = clamp(y, -50, 50)
        z = clamp(z, -50, 50)
        """

        if inst == 'on':
            for a in range(x[0], x[1]+1):
                for b in range(y[0], y[1] + 1):
                    for c in range(z[0], z[1] + 1):
                        on_lights[(a, b, c)] = 'on'
        else:
            for a in range(x[0], x[1]+1):
                for b in range(y[0], y[1] + 1):
                    for c in range(z[0], z[1] + 1):
                        if (a, b, c) in on_lights:
                            del on_lights[(a, b, c)]

    return len(on_lights)


def split_instructions(instruction1, instruction2):
    inst1, x1, y1, z1 = instruction1
    inst2, x2, y2, z2 = instruction2

    if x1[0] > x2[1] or x1[1] < x2[0] or y1[0] > y2[1] or y1[1] < y2[0] or z1[0] > z2[1] or z1[1] < z2[0]:
        return [instruction1, instruction2]
    


instructions, xmin, xmax, ymin, ymax, zmin, zmax = parse_input('22input')
print(xmin, xmax)
print(ymin, ymax)
print(zmin, zmax)
#count = count_lights(instructions)
#print(count)
