def parse_paper(input_filename):
    dots = []
    folds = []
    max_x = -1
    max_y = -1

    with open(input_filename) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            line = line.split(',')
            if len(line) == 2:
                x, y = (int(line[0]), int(line[1]))
                max_x = max(x, max_x)
                max_y = max(y, max_y)
                dots.append((x, y))
            else:
                line = line[0].split()[-1].split('=')
                folds.append((line[0], int(line[1])))

    return dots, folds, max_x, max_y

def hflip_dots(dots, width):
    return [(width-x, y) for x, y in dots]


def vflip_dots(dots, height):
    return [(x, height-y) for x, y in dots]

def xfold_dots(line, dots):
    dots = [(x, y) if x < line else (2*line - x, y) for x, y in dots]
    width = max(x for x, y in dots)
    return dots, width

def yfold_dots(line, dots):
    dots = [(x, y) if y < line else (x, 2*line - y) for x, y in dots]
    height = max(y for x, y in dots)
    return dots, height

def print_dots(dots):
    width = max(x for x, y in dots)
    height = max(y for x, y in dots)
    paper = [[False]*(width+1) for _ in range(height+1)]
    for x, y in dots:
        paper[y][x] = True

    s = ''
    for line in paper:
        for c in line:
            if c:
                s += 'X'
            else:
                s += '.'
        s += "\n"
    print(s)

def apply_folds(dots, folds):
    width = max(x for x, y in dots)
    height = max(y for x, y in dots)
    for axis, line in folds:
        if axis == 'x':
            if line < width/2:
                dots = hflip_dots(dots, width)
                line = width - line
            dots, width = xfold_dots(line, dots)
        else:
            if line < height/2:
                dots = vflip_dots(dots, height)
                line = height - line
            dots, height = yfold_dots(line, dots)
    return dots

dots, folds, width, height = parse_paper('13input')

# Part 1
dots = apply_folds(dots, folds[:1])
print(f"dots after 1 fold: {len(dict.fromkeys(dots))}")

# Part 2
dots = apply_folds(dots, folds[1:])
print_dots(dots)  # UFRZKAUZ

