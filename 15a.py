import numpy as np
import math
import re
from PIL import Image
import cv2





f = open("input_15.txt")
f = open("input_15_sample.txt")

cart = np.zeros((900, 900), dtype=int)

coords = "Sensor at x=(\-?\d+), y=(-?\d+): closest beacon is at x=(\-?\d+), y=(\-?\d+)"

def manhattan_distance(x1,y1,x2,y2):
    return abs(x1-x2) + abs(y1-y2)

row = 10
def von_neumman_neighborhood_cutting_points(x,y,r,row):
    # given the von neumman neighborhood centered in x1,y1 with radius r
    # and a given row, return the numbers of the columns that intersect the edge
    # of the neighborhood in that row

    # if row < y:
    #     x1 = x - (r - (y-row))
    #     x2 = x + (r - (y-row))

    # if row > y:
    #     x1 = x - (r - (row-y))

    if abs(row-y) > r:
        # no intersection, row outside of the neighborhood altogether
        return None,None

    x1 = x - abs(r - abs(y-row))
    x2 = x + abs(r - abs(y-row)) 
    return (x1, x2)

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
for region in known:
    segment = cuts(region[0],region[1],region[2],row)
    if segment[0]:
        discarded.append(segment[0])
        discarded.append(segment[1])

discarded.sort()
print(discarded)

count = 0
rightmost = -math.inf
continuous = False
for i in range(len(discarded)):
    print("rightmost:",rightmost,"i:",discarded[i],"count:",count)
    if i % 2 == 1:
        count += discarded[i]-rightmost + 1
        rightmost = discarded[i] 
    else:
        if discarded[i] == rightmost:
            count -= 1
        else:
            rightmost = discarded[i]
            
#5892813 high

#5367847
#5367846 too low
print(count)

print(cuts(0,7,3,10))
