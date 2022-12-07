import numpy as np


def contains(a,b,c,d):
    if a <= c and b >=d:
        return 1
    if c <= a and d >=b:
        return 1
    return 0


f = open("input_4.txt")
total = 0

for line in f.readlines():
    pairs = line.split(",")
    a = int(pairs[0].split("-")[0])
    b = int(pairs[0].split("-")[1])
    c = int(pairs[1].split("-")[0])
    d = int(pairs[1].split("-")[1])
    total = total + contains(a,b,c,d)
    print(a,b,c,d,contains(a,b,c,d))
print(total)
