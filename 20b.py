import numpy as np
import re
import math
import sys
import logging, sys
from logging import debug as D
from logging import warning as W

np.set_printoptions(threshold=np.inf, linewidth=1000)

def read_input(filename,key=1):
    result = []
    seen = []
    f = open(filename)
    i = 0
    for l in f:
        l.strip()
        result.append(int(l)*key)
        # seen will be rotated and modified, mirroring the data
        # so after any number of operations we can ask where the
        # original item is now (even though there are duplicates!)
        seen.append(i)
        i +=1
    return result, seen

# Note: this could be done with a linked list, 
# but still totally ok (and fast) with lists treated as arrays
def shift_cyclical(a,i,n,s):
    dir = 1 if n > 0 else -1
    inc = 1 if n > 0 else -1
    e = a[i]
#    s[i] = -1 # seen. Only items whose original order have not been processed should have a non neg
    se = s[i]
    nm = (abs(e)) % (len(a)-1)
    if n < 0:
        nm = -nm
    D(f"n:{n},nm:{nm}")
    for x in range(abs(nm)):
        if dir == 1 and i < len(a)-1:
            a[i], a[i+inc] = a[i+inc], a[i]
            s[i], s[i+inc] = s[i+inc], s[i]            
        if dir == 1 and i == len(a)-1:
            a[:] = [e]+a[:-1]
            s[:] = [se]+s[:-1]            
            i = 0
            a[i], a[i+inc] = a[i+inc], a[i]
            s[i], s[i+inc] = s[i+inc], s[i]

        if dir == -1 and i > 1:
            a[i], a[i+inc] = a[i+inc], a[i]
            s[i], s[i+inc] = s[i+inc], s[i]            
        if dir == -1 and i == 1:
            a[i], a[i+inc] = a[i+inc], a[i]
            s[i], s[i+inc] = s[i+inc], s[i]                        
            a[:] = a[1:]+[e]
            s[:] = s[1:]+[se]            
            i = len(a)
        if dir == -1 and i == 0:
            a[:] = a[1:]+[e]
            s[:] = s[1:]+[se]            
            i = len(a)-1
            a[i], a[i+inc] = a[i+inc], a[i]
            s[i], s[i+inc] = s[i+inc], s[i]            
        i += inc
        D(a)
    return i

    
def mix(data,seen):
    for i in range(len(data)):
        D(f"{i} : {data[i]}")
        pos = seen.index(i)
        shift_cyclical(data,pos,data[pos],seen)


def grove_coords(data):
    z = data.index(0)
    D(data)
    D(z)
    D(f"z:{z} len(data):{len(data)}")
    a = data[(z+1000)%len(data)]
    b = data[(z+2000)%len(data)]
    c = data[(z+3000)%len(data)]
    D(f"a:{a},b:{b},c:{c}")
    D(a+b+c)
    return a+b+c


if len(sys.argv) > 1:
    filename = sys.argv[1]
    if len(sys.argv) > 2 and sys.argv[2] == "--debug":
        logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    else:
        logging.basicConfig(stream=sys.stderr, level=logging.WARNING)
else:
    print("usage: python 20.py <filename>")

data, seen = read_input(filename)

mix(data,seen)

print("sum of coordinates (part 1):",grove_coords(data))

data,seen = read_input(filename,811589153)

D(data)

for times in range(0,10):
    mix(data,seen)
    D(f"-------------------------------------------After {times+1} rounds of mixing:")
    D(data)

print("sum of coordinates after 10 shifts (part 2):",grove_coords(data))

