# https://www.sciencedirect.com/science/article/abs/pii/S0377221710002973
import math
import operator
import numpy as np
import easygraph as eg
import graphml2svg
import string
import re
import os
import time

np.set_printoptions(threshold=np.inf, linewidth=1000)

f = open("input_17.txt")
f = open("input_17_sample.txt")



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
        print("|" + "".join(["." if x == 0 else "#" for x in l]) + "|")

n = 0
move =0
jet = 0
highest = 0
while n < 2000: #about enough pieces to determine periodicity
    highest = 0
    for l in tetris:
        highest +=1
        if np.any(l):
            break
    if highest == 0:
        highest = 1
    shape = shapes[n % len(shapes)]
    left = 2
    width = 0
    for each_line in shape:
        if len(each_line) > width:
            width = len(each_line)
    height = len(shape)


    top = highest-1-3-height
    if top < 0:
        tetris = expand_tetris(tetris,-top)
        top = 0
    
    put(tetris, shape, top, left)
    move = 0
    while True:
        move += 1
        if move % 2 == 1:
            if jets[jet] == '>' and left+width <= 6:
                remove(tetris, shape, top, left)
                left += 1
                put(tetris, shape, top, left)
                if np.where(tetris == 2)[0].size > 0:
                    remove(tetris, shape, top, left)
                    left -= 1
                    put(tetris, shape, top, left)
            if jets[jet] == '<' and left > 0:
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
            if top + height >= len(tetris): # bottom
                break
            remove(tetris, shape, top, left)
            top += 1
            put(tetris, shape, top,left)
            if np.where(tetris == 2)[0].size > 0:
                remove(tetris, shape, top, left)
                put(tetris, shape, top - 1,left)
                break
#        print_tetris(tetris)
#        time.sleep(0.1)
#        os.system('clear')

    n += 1
print_tetris(tetris)
#print(len(tetris)+1-highest)
