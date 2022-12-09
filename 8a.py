import re
import numpy as np

List = list

f = open("input_8.txt")


def countVisibleLeft(board: List[List[str]], row: int) -> int:
    l = board[row][0]
    total = 0
    for i in board[row][1:-1]:
        if i > l:
            total = total + 1
            l = i
    return total


def whichVisible(board: List[List[str]], row: int) -> int:
    l = board[row][0]
    total = []
    for i in board[row][1:-1]:
        if i > l:
            total.append()
            l = i
        else:
            total.append(0)
    return total

def visible(l = list[int]) -> list[bool]:
    total = []
    max = l[0]
    for i in l[1:-1]:
        if i > max:
            total.append(True)
            max = i
        else:
            total.append(False)
    return total

def countVisibleTop(board: List[List[str]], col: int) -> int:
    c = [r[col] for r in board]
    return countVisibleLeft([c],0)

def countVisibleBottom(board: List[List[str]], col: int) -> int:
    c = [r[col] for r in board]
    c.reverse()
    return countVisibleLeft([c],0)



def countVisibleRight(board: List[List[str]], row: int) -> int:
    r = board[row].copy()
    r.reverse()
    return countVisibleLeft([r],0)


def scenic(l = list[int]) -> list[bool]:
    total = []
    val = 0
    prev = -1
    for i in l:
        total.append(val)
        if i >= prev:
            val = 1
        else:
            val = val + 1
        prev = i
    return total


a = []
for l in f:
    n = l.strip()
    a.append([int(i) for i in n])

totall = []
totalr = []
totalt = []
totalb = []
for i in range(1,len(a)-1):
    totall.append(visible(a[i]))
    r = a[i].copy()
    r.reverse()
    res_right = visible(r)
    res_right.reverse()
    totalr.append(res_right)


def getcol(board, i):
    return [c[i] for c in board]

for i in range(1,len(a[0])-1):
    c = getcol(a,i)
    print(c)
    totalt.append(visible(c))
    print(visible(c))
    print("---")
    r = c.copy()
    r.reverse()
    print(r)
    res_bottom = visible(r)
    print(res_bottom)
    print("~")
    res_bottom.reverse()
    totalb.append(res_bottom)


left = np.array(totall,bool)
right = np.array(totalr,bool)

top = np.array(totalt,bool)
bottom = np.array(totalb,bool)

top = np.rot90(top)
bottom = np.rot90(bottom)
top = np.flipud(top)
bottom = np.flipud(bottom)

print(left)
print(right)
print(top)
print(bottom)
print("---")

print(left | right | top | bottom)

totalio = np.count_nonzero(left | right | top | bottom)
totalio = totalio + len(a)*2
totalio = totalio + len(a[0])*2
totalio = totalio -4
print(totalio)


print(scenic([4,3,2,0,1,2,3,2]))
