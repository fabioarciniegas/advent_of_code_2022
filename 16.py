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


def solve(solutions,node, budget, state, flow, values):
    solutions[0][state] = max(flow,solutions[0][state])
    for i,candidate in enumerate(values):
        new_budget = budget - distances[node][i] - 1
        if (1 << i) & state or new_budget < 0: # visited or can't visit
            continue
        solve(solutions,i,new_budget,state | (1 <<i),flow + new_budget*values[i],values)
        


def solveIteratively(solutions, s, n, names, distances,budget,values):
    # broken, I use only one row on solutions
    origin = 0
    queue = []
    for i in range(2,budget+1):
        for j,o in enumerate(powers(n)):
            queue.append((o,origin,i))
            while queue:
                e,l,b = queue.pop()
                origin_index = 1 << l
                if e == 0b1111111111:
#                    D(f"not going from {bin(e)=}(last visited through origin {l=}) to {bin(target)=}({target}) by adding {origin_index=} ({origin})")
                    D(solutions)
                    continue
                for k,p in enumerate(powers(n)):
                    new_budget = b - distances[k][l] - 1
                    if j==k or e & p or new_budget < 0: continue
                    queue.append(((e|p),k,new_budget))

                
                flow = max(solutions[b][e],0)
                max_p = 0
                for k,p in enumerate(powers(n)):
                    new_budget = b - distances[k][l] - 1
                    if j==k or e & p or new_budget < 0:
                        continue
                    new_flow = solutions[b-new_budget][e] + values[k] * new_budget
                    if flow < new_flow:
                        flow = new_flow
                        max_p = p
                solutions[b][e|max_p] = flow
                    

def initialize_solutions(G, solutions, n, budget):
    return
    # for j,p in enumerate(powers(n)):
    #     flow = values[j]*i 
    #     solutions[p] = flow            
    



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

names = [g for g in G.nodes]
budget = 30
solutions = np.full((1, 2**len(names)+1), -1, dtype=int)
D(solutions.shape)

floyd = eg.Floyd(G)

s = names.index("AA")
N = len(names)

values = [get_value(G, names[i]) for i in range(N)]
initialize_solutions(G, solutions, N, budget)

distances = np.full((N,N),math.inf,dtype=int)
for i,a in enumerate(floyd):
    for j,b in enumerate(floyd[a]):
        distances[i][j] = floyd[a][b]

solve(solutions, s, budget, 0, 0, values)
print(solutions)
print(np.amax(solutions))
