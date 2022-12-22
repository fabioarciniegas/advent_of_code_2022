import numpy as np
import re
import math
import sys
import logging, sys
from logging import debug as D
from logging import warning as W

np.set_printoptions(threshold=np.inf, linewidth=1000)

def read_input(filename,key=1):
    order = []
    result = []
    seen = []
    f = open(filename)
    for l in f:
        l.strip()
        order.append(int(l)*key)
        result.append(int(l)*key)
        seen.append(0)
    return order, result, seen

def shift3(a,i,n,s):
    dir = 1 if n > 0 else -1
    inc = 1 if n > 0 else -1
    e = a[i]
    s[i] = 1
    se = s[i]
    nm = (abs(e)) % (len(a)-1)
    if n < 0:
        nm = -nm
    if nm == 0 and e!= 0:
        W(f"nm:{nm}, e:{e} i:{i} is multiple of len(a-1) {len(a)-1}")
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
        if dir == 1 and i == len(a):
            W("rare")

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

    
def mix(data,order,seen):
    for e in order:
        D(f"{data} : {e}")
        for pos in [i for i in range(len(data)) if data[i] == e]:
            if seen[pos] == 1:
                continue
            else:
                break
            
        before = len([1 for i in range(len(seen)) if seen[i] == 1])
        shift3(data,pos,e,seen)
        after = len([1 for i in range(len(seen)) if seen[i] == 1])
        if before== after:
            logging.warning("No progress for {e}.")

                    

#        print(f"result of shifting {e} by {e} (in pos {i}):\n{data}")

def grove_coords(data):
    z = data.index(0)
    D(data)
    D(z)
    W(f"z:{z} len(data):{len(data)}")
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

    
#data, order, seen = read_input(filename,811589153)
data, order, seen = read_input(filename)

mix(data,order,seen)

print("sum of coordinates (part 2):",grove_coords(data))

# data = [0,0,0,0,4,0,0]
# seen = [0 for i in range(len(data))]
# shift3(data,4,-20,seen)
# data = [0,0,0,0,4,0,0]
# seen = [0 for i in range(len(data))]
# shift3(data,4,-6,seen)

# data = [0,0,0,0,4,0,0]
# seen = [0 for i in range(len(data))]
# shift3(data,4,20,seen)

# data = [0,0,0,0,4,0,0]
# seen = [0 for i in range(len(data))]
# shift3(data,4,6,seen)

# exit(2)

#print(data)
data,order,seen = read_input(filename,811589153)

for times in range(0,10):
    D(data)
    mix(data,order,seen)
    seen = [0 for i in range(len(data))]
    W(f"-------------------------------------------After {times+1} rounds of mixing:")
    print("sum of coordinates (part 2):",grove_coords(data))
    D(data)
#    print(data)

print("sum of coordinates after 10 shifts (part 2):",grove_coords(data))



#13642
#13972
#4709
# -15291
# dir r  8 7

