import itertools


class Monad:
    def __init__(self, instructions, input):
        self.instructions = instructions
        self.input = input
        self.registers = {}
        for c in 'wxyz':
            self.registers[c] = 0

    def process(self):
        while self.instructions:
            inst = self.instructions.pop(0).split()
            if inst[0] == 'inp':
                self.registers[inst[1]] = self.input.pop(0)
            elif inst[0] == 'add':
                if inst[2] in 'wxyz':
                    self.registers[inst[1]] += self.registers[inst[2]]
                else:
                    self.registers[inst[1]] += int(inst[2])
            elif inst[0] == 'mul':
                if inst[2] in 'wxyz':
                    self.registers[inst[1]] *= self.registers[inst[2]]
                else:
                    self.registers[inst[1]] *= int(inst[2])
            elif inst[0] == 'div':
                if inst[2] in 'wxyz':
                    self.registers[inst[1]] = int(self.registers[inst[1]] / self.registers[inst[2]])
                else:
                    self.registers[inst[1]] = int(self.registers[inst[1]] / int(inst[2]))
            elif inst[0] == 'mod':
                if inst[2] in 'wxyz':
                    self.registers[inst[1]] %= self.registers[inst[2]]
                else:
                    self.registers[inst[1]] %= int(inst[2])
            elif inst[0] == 'eql':
                if inst[2] in 'wxyz':
                    self.registers[inst[1]] = 1 if self.registers[inst[1]] == self.registers[inst[2]] else 0
                else:
                    self.registers[inst[1]] = 1 if self.registers[inst[1]] == int(inst[2]) else 0

        return self.registers['z']



def parse_input(input_filename):
    with open(input_filename) as f:
        instructions = [line.strip() for line in f]
    return instructions



def check_model(model):
    instructions = parse_input('24input')
    input = [int(x) for x in model]
    m = Monad(instructions, input)
    result = m.process()
    if result:
        print(model)
        return True
"""
instructions = parse_input('24inputtest')
input = [14]
m = Monad(instructions, input)
print(m.registers)
"""

models = ["".join(x) for x in itertools.product(["9", "8", "7"], repeat=14)]

for model in models:
    print(len(model))
    if check_model(model):
        break


