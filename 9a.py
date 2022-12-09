import operator
import numpy as np

f = open("input_9.txt")

m = np.zeros((5000,5000))

start = (1999, 1999)
H = start
T = start


def add(t1, t2):
    return tuple(map(operator.add, t1, t2))


def sub(t1, t2):
    return tuple(map(operator.sub, t1, t2))


def neg(t1, t2):
    return tuple(map(operator.neg, t1, t2))


def dist(t1, t2):
    return abs(t1[0] - t2[0]) + abs(t1[1] - t2[1])


def catchups(H, T):
    diff = sub(H, T)
    Ta = [T[0], T[1]]

    if diff[1] == 2:
        Ta[1] = Ta[1] + 1  # T.H → TH
    if diff[1] == -2:
        Ta[1] = Ta[1] - 1
    if diff[0] == 2:
        Ta[0] = Ta[0] + 1
    if diff[0] == -2:
        Ta[0] = Ta[0] - 1
    return (Ta[0], Ta[1])


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

        (1,1) : (0,0),
        (-1,1) : (0,0),
        (-1,-1) : (0,0),
        (1,-1) : (0,0),

        (0,1) : (0,0),
        (0,-1) : (0,0),
        (-1,0) : (0,0),
        (1,0) : (0,0),

        
    }

    return add(T, moveto[diff])


def move(n, H, T, x):
    if n == 0:
        return (H,T)
    H = add(H, x)
    m[T] = 1    
    if dist(H, T) > 0:
        T = catchup(H, T)
    m[T] = 1
    (H,T) = move(n - 1, H, T, x)
    return (H, T)


np.set_printoptions(threshold=np.inf, linewidth=1000)

m[start] = 1
for l in f:
    l.strip()
    d = l[0]
    n = int(l[2:])
    if d == 'R':
        (H, T) = move(n, H, T, (0, 1))
    elif d == 'L':
        (H, T) = move(n, H, T, (0, -1))
    elif d == 'U':
        (H, T) = move(n, H, T, (-1, 0))
    elif d == 'D':
        (H, T) = move(n, H, T, (1, 0))
    print(d,n,H,T)

print(np.count_nonzero(m))
