# https://www.sciencedirect.com/science/article/abs/pii/S0377221710002973 ?
import math
import numpy as np
import easygraph as eg
import re
from easygraph.functions.path import Dijkstra
from easygraph.functions.path import Floyd
import numpy as np
import sys
import logging
from logging import debug as D
from logging import warning as W
from functools import partial

np.set_printoptions(threshold=np.inf, linewidth=1000)


def read_input(filename):
    targets = {}
    f = open(filename)
    G = eg.Graph()
    for l in f:
        l = l.strip()
        r = "^Valve (..) has flow rate=(\d+); tunnels? leads? to valves? (.*)"
        m = re.match(r, l)
        if m:
            G.add_node(m.group(1), node_attr={'flow': m.group(2)})
            targets[m.group(1)] = m.group(3)

    for i in targets.keys():
        r = "(..)\,?\s?"
        t = re.findall(r, targets[i])
        for ti in t:
            G.add_weighted_edge(i, ti, 1)
    return G


def get_value(G, label):
    return int(G.nodes[label]['node_attr']['flow'])


V = get_value


def combinations(r, n):
    """ all bit sets of size N with r bits turned on.
    combinations(3,4) → 0111, 1011, 1101, 1110
    """
    subsets = []
    combos(0, 0, r, n, subsets)
    return subsets


def combos(s, at, r, n, subsets):
    """ backtrack algorithm to generate the power sets"""
    if r == 0:
        subsets.append(s)
    else:
        for i in range(at, n):
            s = s | (1 << i)  # try setting the next bit
            combos(s, i + 1, r - 1, n, subsets)
            # you arrived at all those that contained that bit turned on
            s = s & ~(1 << i)  # now take it off and continue


def notIn(s, subset):
    return ((1 << s) & subset) == 0

def powers(n):
    return [1 << i for i in range(n)]


def solve(solutions, s, n, names, distances,budget):
#    D(n)
    for i in range(2,budget):
        for j in powers(n):
            flow = solutions[i-1][j]
            D(j)
            D("previous")
            for previous in powers(n):
                if previous > j:
                    continue
                previous = previous & ~j
                D(previous)
                
            
        

def solve_1(solutions, s, n, names,distances):
    for r in range(2, n + 1):
        for subset in combinations(r, n):
            if notIn(s, subset):
                continue
            for next_s in range(n):
                if next_s == s or notIn(next_s, subset):
                    continue
                subset_wo_next = subset ^ (1 << next_s)
                maxDist = -math.inf
                for e in range(n):
                    if e == s or e == next_s or notIn(e, subset):
                        continue
                    newDist = solutions[e][subset_wo_next] + m[e][next_s]
                    maxDist = max(maxDist, newDist)

                D(f" {next_s=}  {subset=} with {newDist=}")
                solutions[next_s][subset] = maxDist


def initialize_solutions(G, solutions, start, n):
    for i,j in enumerate(powers(n)):
        solutions[1][j] = get_value(G, names[i])


filename = ""
if len(sys.argv) > 1:
    filename = sys.argv[1]
    if len(sys.argv) > 2 and sys.argv[2] == "--debug":
        logging.basicConfig(stream=sys.stderr,
                            level=logging.DEBUG,
                            format="%(message)s")
    else:
        logging.basicConfig(stream=sys.stderr, level=logging.WARNING)
else:
    print("usage: python 16.py <filename>")

D(f"combinations of 5, 6:{combinations(5,6)=} a.k.a. {[bin(x) for x in combinations(5,6)]}"
  )

G = read_input(filename)

# eg.readwrite.graphviz.write_dot(G, "graph.dot") # TODO: re-enable as a cli option

# node_names_ordered = sorted(
#     [g for g in G.nodes],
#     key=lambda node: int(G.nodes[node]['node_attr']['flow']))

names = [g for g in G.nodes]
budget = 5
solutions = np.zeros((budget, 2**len(names)+1), dtype=int)
D(solutions.shape)

floyd = eg.Floyd(G)

s = names.index("AA")
N = len(names)

initialize_solutions(G, solutions, s, N)

distances = np.full((N,N),math.inf,dtype=int)
#D(type(floyd))
#D(floyd.keys())
for i,a in enumerate(floyd):
    for j,b in enumerate(floyd[a]):
        distances[i][j] = floyd[a][b]
#D(distances)

solve(solutions, s, N, names, distances, budget)
D(solutions)
exit(2)


minCost = findMinCost(m, solutions, s, N, node_names_ordered)

n = len(node_names_ordered)

D(solutions)
D(node_names_ordered)
D(m)
D(solutions[6][1 << 6 | 1 << 0])

end_state = (1 << n) - 1
D(f"{solutions[1][end_state]=}")
D(f"{reconstruct(m,solutions,s,n)=}")

#solve(floyd,solutions,s,n,node_names_ordered)

#print(solutions)
