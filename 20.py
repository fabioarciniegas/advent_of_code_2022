import numpy as np
import re
import math
import sys

np.set_printoptions(threshold=np.inf, linewidth=1000)

def read_input(filename):
    order = []
    result = []
    seen = []
    f = open(filename)
    for l in f:
        l.strip()
        order.append(int(l))
        result.append(int(l))
        seen.append(0)
    return order, result, seen

def shift3(a,i,n,s):
    dir = 1 if n > 0 else -1
    inc = 1 if n > 0 else -1
    e = a[i]
    s[i] = 1
    se = s[i]
    nm = n % len(a)
    for x in range(abs(n)):
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

#    print(s)
    return i

    
def mix(data,order,seen):
    for e in order:
        for pos in [i for i in range(len(data)) if data[i] == e]:
#            print(pos)
            if seen[pos] == 1:
#                print("duplicate",e,pos)
                continue
            else:
                break
            
#        print("doing",e,pos)            
        before = len([1 for i in range(len(seen)) if seen[i] == 1])
#        print(seen)
        
        shift3(data,pos,e,seen)
        after = len([1 for i in range(len(seen)) if seen[i] == 1])
        if before== after:
            print("no progress")
#        print(seen)
                    

#        print(f"result of shifting {e} by {e} (in pos {i}):\n{data}")


if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    print("usage: python 20.py <filename>")

data, order, seen = read_input(filename)
mix(data,order,seen)

#shift3(data,0,-4)
z = data.index(0)
#print(data)
print(z)
a = data[(z+1000)%len(data)]
b = data[(z+2000)%len(data)]
c = data[(z+3000)%len(data)]
print("a,b,c",a,b,c)
print(a+b+c)


#    for i in order:

#13642
#13972
#4709
# -15291
