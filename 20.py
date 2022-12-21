import numpy as np
import re
import math
import sys

np.set_printoptions(threshold=np.inf, linewidth=1000)

def read_input(filename):
    order = []
    result = []
    f = open(filename)
    for l in f:
        l.strip()
        order.append(int(l))
        result.append(int(l))
    return order, result

def shift3(a,i,n):
    dir = 1 if n > 0 else -1
    inc = 1 if n > 0 else -1
    e = a[i]
    nm = n % len(a)
    for x in range(abs(n)):
        if dir == 1 and i < len(a)-1:
            a[i], a[i+inc] = a[i+inc], a[i]
        if dir == 1 and i == len(a)-1:
            a[:] = [e]+a[:-1]
            i = 0
            a[i], a[i+inc] = a[i+inc], a[i]
        if dir == 1 and i == len(a):
            print("ka kaw!!!")
        
        if dir == -1 and i > 1:
            a[i], a[i+inc] = a[i+inc], a[i]
        if dir == -1 and i == 1:
            a[i], a[i+inc] = a[i+inc], a[i]            
            a[:] = a[1:]+[e]
            i = len(a)
        if dir == -1 and i == 0:
            print("ka kaw?")
            a[:] = a[1:]+[e]
            i = len(a)-1
            a[i], a[i+inc] = a[i+inc], a[i]
        i += inc
    return i+= -inc
#        print(a)

    
def mix(data,order):
    seen = {}
    for e in order:
#        print(data,e,":")
        if not e in seen:
            seen[e] = []
        data.findall(e)
        for pos in data.findall(e):
            if pos in seen[e]:
                continue
        shift3(data,pos,e)
#        print(f"result of shifting {e} by {e} (in pos {i}):\n{data}")


if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    print("usage: python 20.py <filename>")

data, order, seen = read_input(filename)
mix(data,order)

#shift3(data,0,-4)
z = data.index(0)
#print(data)
print(z)
a = data[(z+1000)%len(data)]
b = data[(z+2000)%len(data)]
c = data[(z+3000)%len(data)]
print(a,b,c)
print(a+b+c)


#    for i in order:

#13642
#13972
#4709
