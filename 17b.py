# take the reverse output of 17a.py (tac or tail -r)
# the top lines are guaranteed to repeat
# determine the length and start of the periodicity in the file:
f =open("output_17.txt")



lines = []
for l in f:
    l = l.strip()
    lines.append(l)

period = 0
prologue = 0

s = len(lines)//2 # assume the line in the middle is already periodic

p = 1
while period == 0:
    for i in range(p+1):
        if lines[s+i] != lines[s+i+p]:
            p +=1
            break
    if i == p and period < p:
        period = p

print(period)


s = len(lines)-1
pl = 0
while prologue == 0:
    for i in range(1,period+1):
        if lines[s-pl-i] != lines[s-pl-i-period]:
            pl += 1
            break
    if i == period:
        prologue = pl

print(prologue)
