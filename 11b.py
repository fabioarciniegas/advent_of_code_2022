from math import sqrt
from math import lcm

class Monkey(object):

    def __init__(self, items, op, test,  target_a=None, target_b=None):
        self.items = items.copy()
        self.op = op
        self.test = test
        self.target_a = target_a
        self.target_b = target_b
        self.inspected = 0

    def inspect(self, i=0):
        self.items[i] = self.op(self.items[i])
        self.inspected += 1
       
    def bored_of(self, i=0):
        self.items[i] %= self.lcm

    def set_lcm(self, n):
        self.lcm = n

    def throw(self, i=0):
        element = self.items[i]
        del self.items[i]
        if element % self.test == 0:
            self.target_a.catch(element)
        else:
            self.target_b.catch(element)

    def catch(self, item):
        self.items.append(item)

    def set_target_a(self, monkey):
        self.target_a = monkey

    def set_target_b(self, monkey):
        self.target_b = monkey

    def set_targets(self, a, b):
        self.target_a = a
        self.target_b = b

    def turn(self):
        while self.items:
            self.inspect()
            self.bored_of()
            self.throw()


monkeys = [
    Monkey([74, 64, 74, 63, 53], lambda old: old * 7, 5),
    Monkey([69, 99, 95, 62], lambda old: old * old, 17),
    Monkey([59, 81], lambda old: old + 8, 7),
    Monkey([50, 67, 63, 57, 63, 83, 97], lambda old: old + 4, 13),
    Monkey([61, 94, 85, 52, 81, 90, 94, 70], lambda old: old + 3, 19),
    Monkey([69], lambda old: old + 5, 3),
    Monkey([54, 55, 58], lambda old: old + 7, 11),
    Monkey([79, 51, 83, 88, 93, 76], lambda old: old * 3, 2)
]

targets = {
    0: (1, 6),
    1: (2, 5),
    2: (4, 3),
    3: (0, 7),
    4: (7, 3),
    5: (4, 2),
    6: (1, 5),
    7: (0, 6)
}

for i in targets.keys():
    monkeys[i].set_targets(monkeys[targets[i][0]], monkeys[targets[i][1]])

# multiply would work too as they are all primes
# Chinese remainder theorem
lcmi = lcm(*[m.test for m in monkeys])

for m in monkeys:
    m.set_lcm(lcmi)
#print(lcmi)

for round in range(10000):
    print(round)
    for m in monkeys:
        print(m.items)
        m.turn()

monkeys.sort(key=lambda monkey: monkey.inspected, reverse=True)
for m in monkeys:
    print(m.inspected)

print(monkeys[0].inspected * monkeys[1].inspected)
