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


def powers(n):
    return [1 << i for i in range(n)]

# The trick of using an integer to capture the path visited is taken from
# the traveling salesman with dynamic programming:
# https://www.youtube.com/watch?v=cY4HiiFHO1o
#
# a state s is a bit field in which the least significant ith item is on
# if the item i is considered in the state.
#
# x = 2, y = 3 , bit_field_with_both = (1 << 2) | (1 <<3) = 0b110
# 
# In a previous commit I solved this basically using the approach in the
# TSP video and an explicit array. problem was 2^N long array too big
# for memory, whence reusing the trick of bit fields but only as keys into
# a sparse representation (a dict)
#
# Credit to @juanlopes for the most elegant version of this idea which i saw on
# the reddit.
# I did not complete this code before learning from his solution,  I did however figured out the
# solution with an explicit numpy arrray (see previous  commits)
# before I leveraged his idea for a sparse matrix and a nicer recursion than my iterative dynamic
# programming with a huge np matrix .
def solve(solutions,node, budget, state, flow, values):
    solutions[state] = max(flow,solutions.get(state,0))
    for i,new_flow in enumerate(values):
        new_budget = budget - distances[node][i] - 1
        if new_flow == 0 or i == node or (1 << i) & state or new_budget <= 0: # visited or can't visit
            continue
        solve(solutions,i,new_budget,state | (1 <<i),flow + new_budget*new_flow,values)

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
solutions = {} # sparse as opposed to np.full((1, 2**len(names)+1), -1, dtype=int)

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
print(max(solutions.values()))

solutions_2 = {}
solve(solutions_2, s, 26, 0, 0, values)

different = []

for i,f1 in solutions_2.items():
    for j,f2 in solutions_2.items():
        if not i & j:
            different.append(f1+f2)

            
print(max(different))
