import math
import operator
import numpy as np
import easygraph as eg
import string
from easygraph.functions.path import Dijkstra
from easygraph.functions.path import Floyd

alphabet = list(string.ascii_letters)
shortest_path_length = math.inf


def dist(t1, t2):
    return alphabet.index(cart[t1]) - alphabet.index(cart[t2])


def candidates(cart, cur):
    c = []
    if (cur[1] < cart.shape[1] - 1):
        c.append(add(cur, (0, 1)))
    if (cur[1] > 0):
        c.append(add(cur, (0, -1)))
    if (cur[0] > 0):
        c.append(add(cur, (-1, 0)))
    if (cur[0] < cart.shape[0] - 1):
        c.append(add(cur, (1, 0)))
    return c

#used in part 1, too slow for part 2
def BFS(cart, cur, E, steps):
    global shortest_path_length
    c = candidates(cart, cur)
    queue = []
    visited[cur] = True
    if cur == E:
        if steps < shortest_path_length:
            shortest_path_length = steps
    for ci in c:
        if not visited[ci] and dist(ci, cur) <= 1:
            queue.append(ci)
    for q in queue:
        BFS(cart, q, E, steps + 1)
        visited[q] = False
    visited[cur] = False


def add(t1, t2):
    return tuple(map(operator.add, t1, t2))


f = open("input_12.txt")
aap = []
for l in f:
    l = l.strip()
    aap.append([c for c in l])

cart = np.array(aap)

SX = np.where(cart == 'S')
EX = np.where(cart == 'E')

S = (SX[0][0], SX[1][0])
E = (EX[0][0], EX[1][0])

cart[S] = 'a'
cart[E] = 'z'

def generateGraph(cart):
    G = eg.DiGraph()
    for i in range(cart.shape[0]):
        for j in range(cart.shape[1]):
            G.add_node((i, j), node_attr={'letter': cart[i][j]})
            for c in candidates(cart, (i, j)):
                weight = dist(c, (i, j))
                if weight == 1:
                    G.add_weighted_edge((i, j), c, 1)
                elif weight <= 0:
                    G.add_weighted_edge((i, j), c, 1)
    return G


G = generateGraph(cart)

all_as = np.where(cart == 'a')
all_a_pos = []
for i in range(len(all_as[0])):
    a = (all_as[0][i], all_as[1][i])
    all_a_pos.append(a)

all_dists = []
for a in all_a_pos:
    distances = eg.Dijkstra(G, a)
    if E in distances:
        all_dists.append(distances[E])

all_dists.sort()
print(all_dists[0])
