import sys
import re
import pprint
from logging import warning as W
from logging import debug as D
import logging


class Monkey(object):

    def __init__(self, name, number=None, operand="!", left="", right=""):
        self.operand = operand
        self.name = name
        self.left = left
        self.right = right
        self.number = number
        self.complete = False

    def mark_complete(self):
        if self.operand == "!":
            self.complete = self.number
        else:
            lc = self.left.mark_complete()
            rc = self.right.mark_complete()
            self.complete = lc and rc
        return self.complete

    def reverse(self, value=None):
        D(f"self: {self} value: {value}")

        if self.operand == "!":
            if not self.number:
                self.number = value
                D(f"probably hmn {value}")
            return
    
        unknown = self.right if self.left.complete else self.left
        known = self.right if unknown == self.left else self.left
        v = known.evaluate()

        if self.operand == "=":
            unknown.reverse(v)
            return

        if self.operand == "-":
            if unknown == self.left:
                unknown.reverse(value + v)
            else:
                W("This should never happen. Monkeys speak only in non negative numbers !?")
                unknown.reverse(abs(value - v))

        if self.operand == "+":
            unknown.reverse(value - v)

        if self.operand == "*":
            unknown.reverse(value / v)

        if self.operand == "/":
            if unknown == self.left:
                unknown.reverse(value * v)
            else:
                unknown.reverse(v / value)

    def resolved(self):
        return (self.operand == "!"
                and self.number != None) or (type(self.left) != str
                                             or type(self.right) != str)

    def evaluate(self):
        if not self.resolved():
            return None
        if self.operand == "!":
            return self.number
        if self.operand == "+":
            return self.left.evaluate() + self.right.evaluate()
        if self.operand == "-":
            return self.left.evaluate() - self.right.evaluate()
        if self.operand == "*":
            return self.left.evaluate() * self.right.evaluate()
        if self.operand == "/":
            return self.left.evaluate() / self.right.evaluate()
        if self.operand == "=":
            return 1 if self.left.evaluate() == self.right.evaluate() else 0

    def __str__(self):
        return f"{'I' if not self.complete else 'C'} {self.name} {self.number if self.operand == '!' else ''} {self.left.name if type(self.left) == Monkey else self.left+'?'} {self.operand} {self.right.name if type(self.right) == Monkey else self.right+'?'}"


def read_input(filename, bag_o_monkeys):
    f = open(filename)
    type_num = "(.+): (\d+)"
    type_op = "(.+):\s(\S+)\s([\-\+\/\*])\s(\S+)"
    for l in f:
        l.strip()
        m = re.match(type_num, l)
        if m:
            bag_o_monkeys.append(Monkey(m.group(1), int(m.group(2))))
        else:
            m = re.match(type_op, l)
            new_monkey = Monkey(m.group(1),
                                None,
                                operand=m.group(3),
                                left=m.group(2),
                                right=m.group(4))
            bag_o_monkeys.append(new_monkey)


def resolve_monkeys(bom):
    root = None
    humn = None
    for m in bom:
        if m.name == "root":
            root = m
        if m.name == "humn":
            humn = m
        if not m.resolved():
            l = next((x for x in bom if x.name == m.left), "")
            r = next((x for x in bom if x.name == m.right), "")
            m.left = l
            m.right = r
    return root, humn


filename = ""
bag_o_monkeys = []

if len(sys.argv) > 1:
    filename = sys.argv[1]
    if len(sys.argv) > 2 and sys.argv[2] == "--debug":
        logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    else:
        logging.basicConfig(stream=sys.stderr, level=logging.WARNING)
else:
    print("usage: python 21.py <filename>")

read_input(filename, bag_o_monkeys)
D("before resolving")
for m in bag_o_monkeys:
    D(m)

root, humn = resolve_monkeys(bag_o_monkeys)
print("part 1:", root.evaluate())

# change in rules!
root.operand = "="
humn.number = None

D("after resolving, before completing")
for m in bag_o_monkeys:
    D(m)

root.mark_complete()

D("after completing")
for m in bag_o_monkeys:
    D(m)

root.reverse()
D("after reversing")
for m in bag_o_monkeys:
    D(m)

print("part 2:",humn.number)
