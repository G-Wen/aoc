def parse_input(input_filename):
    with open(input_filename) as f:
        return [line.strip() for line in f.readlines()]


def score_line(line, type=None):
    stack = []
    points = {
        '>': 25137,
        '}': 1197,
        ']': 57,
        ')': 3,
    }
    match = {
        '>': '<',
        ']': '[',
        ')': '(',
        '}': '{',
    }
    for char in line:
        if char in '<([{':
            stack.append(char)
        else:
            popped = stack.pop()
            if match[char] != popped:
                return points[char] if type == 'corruption' else -1

    if type == 'corruption':
        return 0

    completion = {
        '<': 4,
        '{': 3,
        '[': 2,
        '(': 1,
    }
    completion_score = 0
    while stack:
        popped = stack.pop()
        completion_score *= 5
        completion_score += completion[popped]
    return completion_score


def score_file(file, type):
    if type == 'corruption':
        score = 0
        for line in file:
            score += score_line(line, type)
        return score
    else:
        completion_scores = [score_line(line) for line in file]
        filtered_scores = [score for score in completion_scores if score >= 0]
        filtered_scores.sort()
        return filtered_scores[len(filtered_scores)//2]


# Part 1
file = parse_input('10input')
corruption_score = score_file(file, 'corruption')
print(f"File corruption score: {corruption_score}")

# Part 2
completion_score = score_file(file, 'completion')
print(f"File completion score: {completion_score}")
