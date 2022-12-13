class DeterministicDice:
    def __init__(self):
        self.rolls = 0
        self.result = 100

    def roll(self):
        self.result %= 100
        self.result += 1
        self.rolls += 1
        return self.result

    def reset(self):
        self.rolls = 0
        self.result = 100


def advance(position, roll):
    roll %= 10
    position += roll
    if position > 10:
        position %= 10
    return position


def simulate_game(p1pos, p2pos, dice, threshold):
    p1score = p2score = 0
    turn = 1
    while p1score < threshold and p2score < threshold:
        rolls = (dice.roll() for _ in range(3))
        if turn == 1:
            p1pos = advance(p1pos, sum(rolls))
            p1score += p1pos
            turn = 2
        else:
            p2pos = advance(p2pos, sum(rolls))
            p2score += p2pos
            turn = 1
    return p1score, p2score, dice.rolls


def combine_outcomes(outcomes):
    current_win = next_win = 0
    for outcome in outcomes:
        current_win += outcome[0]
        next_win += outcome[1]

    return current_win, next_win


def calculate_outcomes(current_player_pos, next_player_pos, current_player_score, next_player_score, table):
    if (current_player_pos, next_player_pos, current_player_score, next_player_score) in table:
        return table[(current_player_pos, next_player_pos, current_player_score, next_player_score)], table

    outcomes = []
    for roll, multiple in dirac_rolls:
        pos_after_roll = advance(current_player_pos, roll)
        score_after_roll = pos_after_roll + current_player_score
        if score_after_roll >= score_to_win:
            outcomes.append((multiple, 0))
        else:
            outcome, table = calculate_outcomes(next_player_pos, pos_after_roll, next_player_score, score_after_roll, table)
            # reverse it because the outcome from above determines the games that the next player wins
            outcomes.append(tuple(reversed((multiple*outcome[0], multiple*outcome[1]))))

    outcome = combine_outcomes(outcomes)
    table[(current_player_pos, next_player_pos, current_player_score, next_player_score)] = outcome
    return outcome, table


# Part 1
deterministic_dice = DeterministicDice()
p1score, p2score, rolls = simulate_game(4, 8, deterministic_dice, 1000)
print(f"Test case: {rolls * min(p1score, p2score)}")

deterministic_dice.reset()
p1score, p2score, rolls = simulate_game(8, 2, deterministic_dice, 1000)
print(f"Part 1: {rolls * min(p1score, p2score)}")

# Part 2
table = {}
score_to_win = 21
dirac_rolls = [(3, 1), (4, 3), (5, 6), (6, 7), (7, 6), (8, 3), (9, 1)]

outcome, table = calculate_outcomes(4, 8, 0, 0, table)
print(f"Test case: {table[(4, 8, 0, 0)]}")

table = {}
outcome, table = calculate_outcomes(8, 2, 0, 0, table)
p1, p2 = table[(8, 2, 0, 0)]
print(f"Part 2: {max(p1, p2)}")
