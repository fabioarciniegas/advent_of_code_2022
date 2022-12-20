import numpy as np
import os
import sys
import time

np.set_printoptions(threshold=np.inf, linewidth=1000)


#f = open("input_17_sample.txt")
f = open("input_17.txt")



tetris = np.ones((0, 7), dtype=int)

jets = f.readline()
jets = jets.strip()

shapes = [
    [[1, 1, 1, 1]],
    [[0, 1, 0], [1, 1, 1], [0, 1, 0]],
    [[0, 0, 1], [0, 0, 1], [1, 1, 1]],
    [[1], [1], [1], [1]],
    [[1, 1], [1, 1]],
]


def expand_tetris(tetris, n=3):
    if n <= 0:
        return tetris
    return np.append(np.zeros((n, 7)), tetris, axis=0)


def put(tetris, shape, x=0, y=2):
    i = 0
    for l in shape:
        tetris[x + i, y:y + len(l)] = np.add(tetris[x + i, y:y + len(l)], l)
        i += 1
    return i


def remove(tetris, shape, x=0, y=2):
    i = 0
    for l in shape:
        tetris[x + i, y:y + len(l)] = np.add(tetris[x + i, y:y + len(l)],
                                             np.negative(l))
        i += 1
    return i


def print_tetris(tetris):
    for l in tetris:
        print("".join(["." if x == 0 else "#" for x in l]))


def first_non_empty(tetris):
    l = 0
    for l in range(len(tetris)):
        if np.any(tetris[l]):
            break
    return l


def tower_height(tetris):
    highest = first_non_empty(tetris)
    th = len(tetris) - highest
    return th


def shape_width(tetris):
    width = 0  # TODO: replace with a numpy idiomatic way
    for each_line in shape:
        if len(each_line) > width:
            width = len(each_line)
    return width


def determine_period(tetris):
    period = 0
    s = len(tetris)//2 # assume the line in the middle is already periodic
    p = 1
    while period == 0:
        for i in range(p+1):
            if not (tetris[s+i] == tetris[s+i+p]).all():
                p +=1
                break
            if i == p and period < p:
                period = p
    return period

def determine_prologue(tetris,period):
    prologue = 0
    s = len(tetris)-1
    pl = 0
    while prologue == 0:
        for i in range(1,period+1):
            if not (tetris[s-pl-i] == tetris[s-pl-i-period]).all():
                pl += 1
                break
            if i == period:
                prologue = pl
    return prologue

    

n = 0
move = 0
jet = 0
highest = 0
prologue_all = 0
period = 0

#1541449275348 too low
shapes_in_period = 0
shapes_out_of_period = 0
blocks_in_prologue = 0
blocks_in_period = 0
blocks_in_reminder = 1600
hint_blocks_in_prologue = 130
lines_in_reminder = 0
goal = 10000

    
mode = sys.argv[1]

animate = mode == "animate"

if mode == "part_1" or mode=="shape":
    goal = int(sys.argv[2])


if mode == "cached":
    goal = 10000
    f =open("output_17.txt")
    lines = []
    for l in f:
        l = l.strip()
        if l == ".......":
            continue
        as_zeros = [ 0 if c == '.' else 1 for c in l]
        tetris = np.append(tetris, [as_zeros],axis=0)
    print("cached")
    print(tetris.shape)
    # at this point we have the trimmed (no overhead empty space)
    # tetris produced by iterating 10000 blocks. Plenty to determine
    # periodicity and prologue
    period = determine_period(tetris)
    prologue_all = determine_prologue(tetris,period)
    
    # return to an empty tetris
    tetris = np.ones((0, 7), dtype=int)

def put_n_shapes(tetris,n):
    while n < goal:
        highest = first_non_empty(tetris)
        shape = shapes[n % len(shapes)]
        left = 2
        width = shape_width(shape)
        height = len(shape)

        top = highest - 3 - height # start next shape 3 drom the highest
    #    print(highest,top)

        if top < 0:
            tetris = expand_tetris(tetris, -top)
            top = 0

        put(tetris, shape, top, left)

        move = 0
        while True:
            move += 1
            if move % 2 == 1:
                if jets[jet] == '>' and left + width <= 6:
                    #                print("right")
                    remove(tetris, shape, top, left)
                    left += 1
                    put(tetris, shape, top, left)
                    if np.where(tetris == 2)[0].size > 0:
                        remove(tetris, shape, top, left)
                        left -= 1
                        put(tetris, shape, top, left)
                if jets[jet] == '<' and left > 0:
                    #                print("left")
                    remove(tetris, shape, top, left)
                    left -= 1
                    put(tetris, shape, top, left)
                    if np.where(tetris == 2)[0].size > 0:
                        remove(tetris, shape, top, left)
                        left += 1
                        put(tetris, shape, top, left)
                jet += 1
                if jet == len(jets):
                    jet = 0

            else:
                #           print("dropping")
                if top + height >= len(tetris):  # bottom
                    break
                remove(tetris, shape, top, left)
                top += 1
                put(tetris, shape, top, left)
                if np.where(tetris == 2)[0].size > 0:
                    remove(tetris, shape, top, left)
                    put(tetris, shape, top - 1, left)
                    break
            if (animate):
                print_tetris(tetris)
                time.sleep(0.6)
                os.system('clear')

            if mode == "cached":
                if blocks_in_prologue == 0 and tower_height(tetris) == prologue_all:
                    blocks_in_prologue = n

                if tower_height(tetris) == prologue_all + period:
                    if n - blocks_in_prologue > blocks_in_period:
                        blocks_in_period = n - blocks_in_prologue
        n += 1

if mode == "cached":
    print("prologue:",prologue_all)    
    print("blocks_in_prologue:",blocks_in_prologue)
    print("blocks_in_period:", blocks_in_period)    
    goal = 1000000000000
#    goal -= blocks_in_prologue
    periodic_blocks = goal // blocks_in_period
    print("period:",period)
    print("full periods to goal:",periodic_blocks)
    print("lines covered by periodic blocks:",periodic_blocks*period)
    extra_blocks = goal % blocks_in_period
    print("extra blocks",extra_blocks)
    print("run python 17a.py part_1 <extra blocks> and add to lines covered ")
    
if mode == "part_1":
    print(tower_height(tetris))
    
if mode == "print" or mode == "":
    print_tetris(tetris)

if mode == "shape":
    print("shape:",tetris.shape)
    print("tower_height:",tower_height(tetris))


# 1542343387626 wrong
# 1542343387683
# 1542343387474
# 1542343387394
# 1542343387476
# 1542343387267
# 1542343387472

#1542343387476


#     if th == prologue_ends:
#         blocks_in_prologue = n
#         print(blocks_in_prologue, " blocks in prologue")
#     if th == prologue_ends + period:
#         print(len(tetris), highest, th, prologue_ends)
#         blocks_in_period = n - blocks_in_prologue
#         print(blocks_in_period, " blocks in period")

#     if n == hint_blocks_in_prologue + blocks_in_period + blocks_in_reminder + 1:
#         lines_in_reminder = th - period - prologue_ends

# a = ((1000000000000)//blocks_in_period)*period
# print(1000000000000%blocks_in_period," blocks in reminder")
# print(a)
# #print((1000000000000-prologue_ends)%blocks_in_period*lines_in_reminder)
# print(lines_in_reminder)
# print(a+lines_in_reminder)
# print(1514285714288)
