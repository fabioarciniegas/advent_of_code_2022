import math
import numpy as np
import easygraph as eg
import re
import sys
import logging
from logging import debug as D

np.set_printoptions(threshold=np.inf, linewidth=1000)


def read_input(filename):
    f = open(filename)
    return [l.strip() for l in f]


def snafu2dec(s):
    d = {"2": 2, "1": 1, "0": 0, "-": -1, "=": -2}
    total = 0
    for p, i in enumerate(s[::-1]):
        total += d[i] * 5**p
    return total

def dec2snafu(n):
    d = {2: "2", 1: "1", 0: "0", 3: "1=", 4: "1-"}
    b5 = []
    while n > 0:
        b5.insert(0,n%5)
        n = n // 5
    snafu = []
    carry = 0
    D(b5)
    for i,e in enumerate(b5[::-1]):
        e += carry
        carry = e // 5
        g = e%5
        if len(d[g]) > 1:
            snafu.insert(0,d[g][-1])
            carry += 1
        else:
            snafu.insert(0,d[g])
    return "".join([str(i) for i in snafu])


filename = ""
if len(sys.argv) > 1:
    filename = sys.argv[1]
    if len(sys.argv) > 2 and sys.argv[2] == "--debug":
        logging.basicConfig(stream=sys.stderr,
                            level=logging.DEBUG,
                            format="%(message)s")
    else:
        logging.basicConfig(stream=sys.stderr, level=logging.WARNING)
else:
    print("usage: python 25.py <filename>")

snafu = read_input(filename)

code = sum([snafu2dec(i) for i in snafu])
print(code)
print(dec2snafu(code))

