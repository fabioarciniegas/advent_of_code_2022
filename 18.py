import numpy as np
import re
import math
import sys

np.set_printoptions(threshold=np.inf, linewidth=1000)

# passing filename cleaner with sys.argv for once in aoc
#f = open("inside.txt")

max_x, max_y, max_z = -math.inf, -math.inf, -math.inf
min_x, min_y, min_z = math.inf, math.inf, math.inf


def adjecents(c, maxes):
    adj = []
    x, y, z = c[0], c[1], c[2]
    mx, my, mz = maxes[0], maxes[1], maxes[2]
    if x < mx:
        adj.append((x + 1, y, z))
    if x > 0:
        adj.append((x - 1, y, z))
    if y < my:
        adj.append((x, y + 1, z))
    if y > 0:
        adj.append((x, y - 1, z))
    if z < mz:
        adj.append((x, y, z + 1))
    if z > 0:
        adj.append((x, y, z - 1))
    return adj


def surface(cubes, coordinates, maxes):
    edges = 0
    for c in coordinates:
        for adj in adjecents(c, maxes):
            if cubes[adj] == 1:
                edges += 1 # each edge will be counted twice, once per adjecent cube
    return len(coordinates) * 6 - edges


def read_input(filename):
    f = open(filename)
    coords = []
    max_x, max_y, max_z = -math.inf, -math.inf, -math.inf
    min_x, min_y, min_z = math.inf, math.inf, math.inf
    input_format = "(\d+),(\d+),(\d+)"
    for l in f:
        m = re.match(input_format, l)
        x, y, z = int(m.group(1)), int(m.group(2)), int(m.group(3))
        # a small redundancy to avoid asking for keys twice
        coords.append((x, y, z))
        max_x = max(x, max_x)
        max_y = max(y, max_y)
        max_z = max(z, max_z)
        min_x = min(x, min_x)
        min_y = min(y, min_y)
        min_z = min(z, min_z)

    cubes = np.zeros((max_x + 1, max_y + 1, max_z + 1), dtype=int)
    for p in coords:
        cubes[p[0], p[1], p[2]] = 1

    return cubes, coords, (max_x, max_y, max_z)

def flood_fill(cubes,maxes,start=(0,0,0)):
    queue = [start]
    while queue:
        next_coord = queue.pop()
        cubes[next_coord] = 2
        for adj in adjecents(next_coord,maxes):
            if cubes[adj] == 0:
                queue.append(adj)

def pockets(cubes):
    cubes[np.where(cubes == 0)] = 3
    cubes[np.where(cubes < 3)] = 0
    cubes[np.where(cubes == 3)] = 1        

if len(sys.argv) > 1:
    cubes, coords, maxes = read_input(sys.argv[1])
    s = surface(cubes,coords,maxes)
    print("surface:", s )
    flood_fill(cubes,maxes)
    pockets(cubes)
    c = np.where(cubes == 1)
    coords = []
    for i in range(len(c[0])):
        coords.append((c[0][i],c[1][i],c[2][i]))
    p = surface(cubes,coords,maxes)
    print("discarding pockets:",s-p)
else:
    print("usage: python 18.py [filename]")
