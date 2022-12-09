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
    for i in range(len(l)):
        run = 1
        j = i-1
        while(j>0 and l[j]<l[i]):
            run = run +1
            j = j-1
        total.append(run)
    total[0]=0
    return total


a = []
for l in f:
    n = l.strip()
    a.append([int(i) for i in n])

totall = []
totalr = []
totalt = []
totalb = []
for i in range(len(a)):
    totall.append(scenic(a[i]))
    r = a[i].copy()
    r.reverse()
    res_right = scenic(r)
    res_right.reverse()
    totalr.append(res_right)


def getcol(board, i):
    return [c[i] for c in board]

for i in range(len(a[0])):
    c = getcol(a,i)
    totalt.append(scenic(c))
    r = c.copy()
    r.reverse()
    res_bottom = scenic(r)
    res_bottom.reverse()
    totalb.append(res_bottom)


left = np.array(totall,int)
right = np.array(totalr,int)

top = np.array(totalt,int)
bottom = np.array(totalb,int)

top = np.rot90(top)
bottom = np.rot90(bottom)
top = np.flipud(top)
bottom = np.flipud(bottom)

np.set_printoptions(threshold=np.inf,linewidth=1000)
print(left)
print(right)
print(top)
print(bottom)
print("---")

print(left.shape,right.shape,top.shape,bottom.shape,)

a = np.multiply(left,right)
b = np.multiply(top,bottom)
c = np.multiply(a,b)

print(c)
print(np.amax(c))

