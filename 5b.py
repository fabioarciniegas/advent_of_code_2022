import numpy as np
import re

f = open("input_5.txt")
crates = [[],[],[],[],[],[],[],[],[]]

def move_one(x,y):
    crates[y].append(crates[x].pop())


#def move_n(x,y,n):
#    if n <= 0:
#        return
#    move_one(x,y)
#    move_n(x,y,n-1)

def move_n(x,y,n):
    c = crates[x][-n:]
    crates[y].extend(c)
    crates[x] = crates[x][:len(crates[x])-n]

for l in f:
    last= 0
    if l.strip() == "":
        break
    while l != "" and last != -1:
        last = l.find("[",last)
        if last != -1:
            crates[last//4].insert(0,l[last+1])
            last = last + 1

for l in f:
    x = l.strip()
    rx = "^move\s+(\d+)\s+from\s+(\d+)\s+to\s+(\d+)"
    if re.match(rx,x) == None:
        continue
    m = re.search(rx,x)
    move_n(int(m.group(2))-1,int(m.group(3))-1,int(m.group(1)))

for c in crates:
    print(c[-1] if len(c)>0 else " ",end="")
print()

# 1224
