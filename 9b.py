import operator
import numpy as np

f = open("input_9.txt")

m = np.zeros((5000, 5000))

start = (1999, 1999)
rope = [start, start, start, start, start, start, start, start, start, start]


def add(t1, t2):
    return tuple(map(operator.add, t1, t2))


def sub(t1, t2):
    return tuple(map(operator.sub, t1, t2))


def catchup(H, T):
    diff = sub(H, T)
    moveto = {
        (0, 2): (0, 1),
        (0, -2): (0, -1),
        (2, 0): (1, 0),
        (-2, 0): (-1, 0),
        (-2, 1): (-1, 1),
        (-1, 2): (-1, 1),
        (1, 2): (1, 1),
        (2, 1): (1, 1),
        (2, -1): (1, -1),
        (1, -2): (1, -1),
        (-1, -2): (-1, -1),
        (-2, -1): (-1, -1),
        (1, 1): (0, 0),
        (-1, 1): (0, 0),
        (-1, -1): (0, 0),
        (1, -1): (0, 0),
        (0, 1): (0, 0),
        (0, -1): (0, 0),
        (-1, 0): (0, 0),
        (1, 0): (0, 0),
        (0, 0): (0, 0),
        
        (-2,2): (-1,1),
        (-2,-2): (-1,-1),
        (2,2) : (1,1),
        (2,-2): (1,-1)
    }

    return (H,add(T, moveto[diff]))


def movehead(H, x):
    H = add(H, x)
    return H


np.set_printoptions(threshold=np.inf, linewidth=1000)

m[start] = 1
for l in f:
    l.strip()
    d = l[0]
    n = int(l[2:])
    while n > 0:
        print(d)
        if d == 'R':
            rope[9] = movehead(rope[9], (0, 1))
        elif d == 'L':
            rope[9] = movehead(rope[9], (0, -1))
        elif d == 'U':
            rope[9] = movehead(rope[9], (-1, 0))
        elif d == 'D':
            rope[9] = movehead(rope[9], (1, 0))
        for i in range(9, 0, -1):
            print(rope)
            (rope[i], rope[i - 1]) = catchup(rope[i], rope[i - 1])
            m[rope[0]]=1
        n = n - 1

print(np.count_nonzero(m))
