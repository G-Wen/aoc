def advance(position, roll):
    position += roll
    if position > 10:
        position %= 10
    return position


