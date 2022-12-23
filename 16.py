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

def set_value(G, label,value):
    G.nodes[label]['node_attr']['flow'] = value


def max_flow(capacity, labels,G,from_node):
    solutions = np.zeros((len(labels) + 1, capacity + 1))

    # base case of i=0. IF we were not using np.zeros would have to be explicit:
    #for c in range(capacity+1):
    #        solutions[0][c] = 0 
    for i in range(1, len(labels)+1):
        cur_label = labels[i-1]
        s_is = eg.Dijkstra(G, from_node)        
        for c in range(capacity+1):
            s_i = s_is[labels[i-2]] + 1
            D(f"from {from_node=} to {labels[i-2]=} : {s_i=}")
            v_i = get_value(G,cur_label)
            D(f"{cur_label=}{s_is=}{s_i=}{v_i=}")
            if s_i > c:
                solutions[i][c] = solutions[i-1][c]
            else:
                a = solutions[i][c] = solutions[i-1][c]
                b = solutions[i-1][c - s_i] + v_i
                solutions[i][c] = max(a,b)
#                if b > a:
#                    set_value(G,cur_label,0)
#                    from_node = cur_label



                
    return solutions[len(items)][capacity], solutions


    #         max_label = None
    #         for label in labels:
    #             if s_is[label] + 1 > c:
    #                 continue
    #             walking = s_is[label]
    #             candidate = solutions[i-1][c - walking] + v_i*(capacity-c)
    #             if candidate > max_f_wrt_current:
    #                 max_f_wrt_current = candidate
    #                 max_label = label
    #         solutions[i][c] = max_f_wrt_current
    #         if max_label:
    #             flows[labels.index(max_label)] = 0
    # return solutions[len(items)][capacity], solutions


filename = ""
if len(sys.argv) > 1:
    filename = sys.argv[1]
    if len(sys.argv) > 2 and sys.argv[2] == "--debug":
        logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    else:
        logging.basicConfig(stream=sys.stderr, level=logging.WARNING)
else:
    print("usage: python 16.py <filename>")

G = read_input(filename)

eg.readwrite.graphviz.write_dot(G, "graph.dot")

items = [g for g in G.nodes]
x,solutions = max_flow( 30,items,G,"AA")
print(x)
print(solutions)


exit(2)


def reconstruct_knapsack(A, items, capacity):
    S = []
    c = capacity
    for i in range(len(items), 0, -1):
        s_i = items[i - 1][1]
        v_i = items[i - 1][0]
        #        print(i-1,v_i,s_i)
        if s_i <= c and A[i][c - s_i] + v_i >= A[i][c]:
            S.append(i - 1)
            c = c - s_i
    return S



def best_move(G, start, steps_left=30):
    nodes = G.nodes
    dk = eg.Dijkstra(G, start)
    gains = []
    distances = []
    names = []
    for i in dk.keys():
        gains.append(int(nodes[i]['node_attr']['flow']))
        distances.append(dk[i])
        names.append(i)
    max_gain_ot = -math.inf
    max_ = None
    max_distance = min(max(distances), steps_left)
    for i in range(len(distances)):
        throughput = (steps_left - distances[i] + 1) * gains[i]
        print(names[i], throughput, "(", steps_left, "-", distances[i], ")*",
              gains[i])
        if throughput > max_gain_ot:
            max_ = i
            max_gain_ot = throughput
    print("therefore", names[max_])
    return names[max_], distances[max_]


mins = 30
pos = "AA"
pressure = 0
total = 0
dist = 0

# pos,dist = best_move(G, pos, mins)
# while mins > 0:
# #    print(30-mins+1,pos,"?" if dist else "",dist,pressure,total)
#     total += pressure
#     mins -= 1
#     if dist:
#         dist -= 1 # use the minute walking
#         continue
#     else:
#         pressure += int(G.nodes[pos]['node_attr']['flow'])
#         G.nodes[pos]['node_attr']['flow'] = 0
#         pos,dist = best_move(G, pos, mins)

shortest_path = eg.Dijkstra(G, "AA")
item_labels = [x for x in shortest_path.keys()]
items = []
for label in shortest_path.keys():
    items.append([get_value(G, label), shortest_path[label]])

print(items)
print(item_labels)

while mins > 0:
    investment, solutions = knapsack(5, items)
    S = reconstruct_knapsack(solutions, items, 5)
    print(S)
    print(item_labels[S[0]])
    mins -= investment
