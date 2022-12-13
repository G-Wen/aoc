def parse_input(input_filename):
    with open(input_filename) as f:
        iea = ['1' if c == '#' else '0' for c in f.readline().strip()]
        f.readline()
        image = {}
        for y, line in enumerate(f):
            line = line.strip()
            for x, c in enumerate(line):
                image[(x, y)] = '1' if c == "#" else '0'
        return iea, image, (0, x), (0, y)


def display(image, xdim, ydim):
    rows = [[image[(x,y)] for x in range(xdim[0], xdim[1]+1)] for y in range(ydim[0], ydim[1]+1)]
    for row in rows:
        print("".join(['#' if c == '1' else '.' for c in row]))


def pad_image(image, xdim, ydim, pad_size, char):
    xmin, xmax = xdim
    ymin, ymax = ydim

    for x in range(xmin-pad_size, xmin):
        for y in range(ymin-pad_size, ymax+pad_size+1):
            image[(x,y)] = char
    for x in range(xmax+1, xmax+pad_size+1):
        for y in range(ymin - pad_size, ymax+pad_size+1):
            image[(x, y)] = char
    for y in range(ymin-pad_size, ymin):
        for x in range(xmin-pad_size, xmax+pad_size+1):
            image[(x,y)] = char
    for y in range(ymax+1, ymax+pad_size+1):
        for x in range(xmin-pad_size, xmax+pad_size+1):
            image[(x,y)] = char
    xdim = (xmin-pad_size, xmax+pad_size)
    ydim = (ymin-pad_size, ymax+pad_size)

    return image, xdim, ydim


def apply_iea(image, iea, xdim, ydim):
    new_image = {}

    for x in range(xdim[0]+1, xdim[1]):
        for y in range(ydim[0]+1, ydim[1]):
            index = int("".join([image[(nx, ny)] for ny in range(y-1, y+2) for nx in range(x-1, x+2)]), 2)
            new_image[(x, y)] = iea[index]
    xdim = (xdim[0]+1, xdim[1]-1)
    ydim = (ydim[0]+1, ydim[1]-1)

    return new_image, xdim, ydim


def enhance_image(image, xdim, ydim, steps):
    for step in range(steps):
        if iea[0] == '0':
            pad_char = '0'
        else:
            pad_char = str(step % 2) if iea[-1] == '0' else '1'

        image, xdim, ydim = pad_image(image, xdim, ydim, 2, pad_char)
        image, xdim, ydim = apply_iea(image, iea, xdim, ydim)

    return image, xdim, ydim


iea, image, xdim, ydim = parse_input('20input')

image, xdim, ydim = enhance_image(image, xdim, ydim, 2)
print(f"Part 1: {sum([int(v) for v in image.values()])}")

image, xdim, ydim = enhance_image(image, xdim, ydim, 48)
print(f"Part 2: {sum([int(v) for v in image.values()])}")
