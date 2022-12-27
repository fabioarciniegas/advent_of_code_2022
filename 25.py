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

print(sum([snafu2dec(i) for i in snafu]))

D(snafu2dec("1=-0-2"))
