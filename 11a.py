class Monkey(object):

    def __init__(self, items, op, test, target_a=None, target_b=None):
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
        self.items[i] = self.items[i] // 3

    def throw(self, i=0):
        element = self.items[i]
        del self.items[i]
        if self.test(element):
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
    Monkey([74, 64, 74, 63, 53],
           lambda old: old * 7,
           lambda item: item % 5 == 0),
    Monkey([69, 99, 95, 62],
           lambda old: old * old,
           lambda item: item % 17 == 0),
    Monkey([59, 81],
           lambda old: old + 8,
           lambda item: item % 7 == 0),
    Monkey([50, 67, 63, 57, 63, 83, 97],
           lambda old: old + 4,
           lambda item: item % 13 == 0),
    Monkey([61, 94, 85, 52, 81, 90, 94, 70],
           lambda old: old + 3,
           lambda item: item % 19 == 0),
    Monkey([69],
           lambda old: old + 5,
           lambda item: item % 3 == 0),
    Monkey([54, 55, 58],
           lambda old: old + 7,
           lambda item: item % 11 == 0),
    Monkey([79, 51, 83, 88, 93, 76],
           lambda old: old * 3,
           lambda item: item % 2 == 0),
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

for round in range(20):
    for m in monkeys:
#        print(m.items)
        m.turn()

monkeys.sort(key=lambda monkey: monkey.inspected,reverse=True)
for m in monkeys:
    print(m.inspected,end=",")
    
print(monkeys[0].inspected * monkeys[1].inspected)
