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


def set_value(G, label, value):
    G.nodes[label]['node_attr']['flow'] = value


def max_with_budget(i, labels, solutions, floyd, budget, current):
    D(f"{budget=}")
    max_value = solutions[i][budget - 1]

    while budget:
        candidates = [
            cl for cl in labels
            if floyd[current][cl] <= budget and floyd[current][cl] != 0
        ]
        D(f"Candidates from {current=} are {candidates=}")
        for candidate in candidates:
            max_candidate_value = 0
            value = 0
            candidate_index = items.index(candidate)
            d = floyd[current][candidate]
            D(f"{current=} {candidate=} {candidate_index=}, {budget=} {d=}")
            value = solutions[candidate_index][
                budget -
                d]  #+ max_with_budget(candidate_index-1,labels,solutions,floyd,budget-d,candidate)
            if value > max_candidate_value:
                max_candidate = candidate_index
                max_budget_decrease = d
                max_candidate_value = value

        D(f"{max_value=}")
    return max_value


def max_w_budget2(i, b, labels, solutions, floyd, seen=[], skip_first=False):
    option_1 = solutions[i][b - 1]
    #max that I can reach in d steps plus what I can reach from there in another b-d steps
    possible_maxes = []
    possible_maxes.append(option_1 if not skip_first else 0)
    current_label = labels[i]
    D(f"{i=} {b=} {seen=}")
    exclude = seen.copy()

    for cl in [x for x in labels if x not in seen]:
        cl_index = labels.index(cl)
        d = floyd[current_label][cl]
        if d <= b and d > 0:
            exclude.append(current_label)
            possible_maxes.append(solutions[i][b - d] + solutions[cl_index][d])


#                                  max_w_budget2(cl_index, b - d,labels,solutions,floyd,exclude,True))
        D(possible_maxes)
        D(solutions)
    return max(possible_maxes)


def max_flow(capacity, labels, G, from_node, floyd):
    solutions = np.zeros((len(labels), capacity + 1))
    #    items = [g for g in G.nodes]
    # base case of i=0. IF we were not using np.zeros would have to be explicit:
    #    for c in range(capacity + 1):
    #        solutions[0][c] = 0
    seen = []
    for i in range(len(labels)):
        solutions[i][1] = get_value(G, labels[i])

    for i in range(0, solutions.shape[0]):
        for c in range(2, solutions.shape[1]):
            solutions[i][c] = max_w_budget2(i, c, labels, solutions, floyd,
                                            seen)

    D(solutions)
    # for c in range(capacity+1):
    #     for i in range(len(labels)):
    #         d = floyd["AA"][labels[i]]
    #         if d <= c:
    #             solutions[1][c] = max(solutions[1][c],get_value(G,labels[i]))

    return 2, solutions


#     last_visited = "AA"

#     for i in range(1, len(labels)+1):
#         cur_label = labels[i-1]
#         for c in range(capacity+1):
#             s_i = floyd["AA"][cur_label] + 1
#             v_i = get_value(G,cur_label)
# #            D(f"{s_i=}{v_i=}")

#             if s_i  > c:
#                 solutions[i][c] = solutions[i-1][c]!
#             else:
#                 solutions[i][c] = max(solutions[i-1][c],
#                                       solutions[i-1][c - s_i] + v_i*(capacity - s_i - c))

#     return solutions[len(items)][capacity], solutions


#def findOptimalTour(floyd,solutions,s,n):
    

def findMinCost(m,solutions,s,n,names):
    # end state is bit mask with N bits sets to 1 (2**n - 1)
    end_state = (1 << n) - 1

    mintourcost = math.inf
    for e in range(n):
        if e == s:
            continue
        tourcost = solutions[e][end_state] + m[e][s]
        mintourcost = min(mintourcost,tourcost)
    return mintourcost


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

def notIn(s,subset):
    return ((1 << s) & subset) == 0

def solve(m, solutions, s, n,names):
    for r in range(3, n):
        for subset in combinations(r, n):
            if notIn(s,subset):
                continue
            for next_s in range(n):
                if next_s == s or notIn(next_s,subset):
                    continue
                subset_wo_next = subset ^ (1 << next_s)
                minDist = math.inf
                for e in range(n):
                    if e == s or e == next_s or notIn(e,subset):
                        continue
                    newDist = solutions[e][subset_wo_next] + m[e][next_s]
                    D(f"considering {names[e]=} and {names[next_s]=} with {newDist=}")
                    minDist=min(minDist,newDist)
                    
                solutions[next_s][subset] = minDist


def initialize_table(m, solution, start, n):
    for i in range(n):
        if i ==  start:
            continue
#        D(f"Distance from {start=}({s=}) to {name=}({i=}): {floyd[start][name]}")
        solutions[i][1 << start | 1 << i] = m[start][i]


def adjecency_matrix(G,ordered_names):
    side = len(G.nodes)
    A = np.full((side,side),10000,dtype=int)
    for i,e in enumerate(ordered_names):
        for s in G.neighbors(node=e):
            j = ordered_names.index(s)
            A[i][j] = G.adj[e][s]['weight']
    return A

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


D(f"combinations of 5, 6:{combinations(5,6)=} a.k.a. {[bin(x) for x in combinations(5,6)]}")
  
G = read_input(filename)

# eg.readwrite.graphviz.write_dot(G, "graph.dot") # TODO: re-enable as a cli option

node_names_ordered = sorted(
    [g for g in G.nodes],
    key=lambda node: int(G.nodes[node]['node_attr']['flow']))
solutions = np.full((len(node_names_ordered), 2**len(node_names_ordered)),
                    10000,
                    dtype=int)

floyd = eg.Floyd(G)
m = adjecency_matrix(G,node_names_ordered)
s = node_names_ordered.index("AA")
N = len(node_names_ordered)

initialize_table(m,solutions,s,N)
solve(m,solutions,s,N,node_names_ordered)
minCost = findMinCost(m, solutions,s,N,node_names_ordered)

n = len(node_names_ordered)

D(solutions)
D(node_names_ordered)
D(m)
D(f"{minCost=}")


#solve(floyd,solutions,s,n,node_names_ordered)





#print(solutions)

