import numpy as np
import math
import re
from PIL import Image
import cv2






f = open("input_15_sample.txt")
f = open("input_15.txt")

cart = np.zeros((900, 900), dtype=int)

coords = "Sensor at x=(\-?\d+), y=(-?\d+): closest beacon is at x=(\-?\d+), y=(\-?\d+)"

def manhattan_distance(x1,y1,x2,y2):
    return abs(x1-x2) + abs(y1-y2)

row = 2000000
def von_neumman_neighborhood_cutting_points(x,y,r,row):
    # given the von neumman neighborhood centered in x1,y1 with radius r
    # and a given row, return the numbers of the columns that intersect the edge
    # of the neighborhood in that row

    if abs(row-y) > r:
        # no intersection, row outside of the neighborhood altogether
        return None,None

    x1 = x - abs(r - abs(y-row))
    x2 = x + abs(r - abs(y-row))
    return (x1, x2)

def overlap(s1,s2):
    if s2[0] <= s1[1] and s2[1] <= s1[1]: # contained
        return -1,s1
    if s2[0] <= s1[1] and s2[1] > s1[1]: # extended
        return 0,(s1[0],s2[1])
    if s2[0] > s1[1]: # no overlap
        return 1,s2


    
cuts = von_neumman_neighborhood_cutting_points

known = []
for l in f:
    m = re.match(coords, l)
    sx = int(m.group(1))
    sy = int(m.group(2))
    bx = int(m.group(3))
    by = int(m.group(4))
    d = manhattan_distance(sx,sy,bx,by)
#    print(sx,sy,bx,by,d)
    known.append([sx,sy,d])

    

discarded = []

for row in range(0,4000000):
    all_in_row = []
    discarded = []
    for beacon in known:
        segment = cuts(beacon[0],beacon[1],beacon[2],row)
        if segment[0]:
            discarded.append((segment[0],segment[1]))
    if not discarded:
        continue
    discarded = sorted(discarded)
    
    curs = discarded[0]
    non_overlapping = []
    for t in discarded[1:]:
        res,rescurs = overlap(curs,t)
        if res == 1:
            non_overlapping.append(curs)
            curs = t
        if res == 0:
            curs = rescurs
        if res == -1:
            continue
    non_overlapping.append(curs)

    if len(non_overlapping) == 2:
        if non_overlapping[1][0] - non_overlapping[0][1] == 2:
            print("x:",non_overlapping[1][0]-1,"y:",row)
            print((non_overlapping[1][0]-1) * 4000000 + row)
            break
