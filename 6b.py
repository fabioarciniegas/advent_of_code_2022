import numpy as np
import re

f = open("input_6.txt")

for l in f:
    i = 14
    print(l[i-14:i])
    while i < len(l):
        s = set(l[i-14:i])
        if len(s) == 14:
            print(i)
            break
        i = i+1
