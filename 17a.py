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

tetris = np.zeros((1, 7), dtype=int)

jets = f.readline()

shapes = [
    [[1, 1, 1, 1]],
    [[0, 1, 0], [1, 1, 1], [0, 1, 0]],
    [[0, 0, 1], [0, 0, 1], [1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1], [1], [1], [1]],
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
    print("---------")


def shift(tetris, amount=1, x=0):
    l = tetris[x]
    ones = np.where(l == 1)[0]
    if amount == 1 and ones[-1] < len(l) - 1:
        l = np.roll(l, amount)
    if amount == -1 and ones[0] > 0:
        l = np.roll(l, amount)
    tetris[x, :] = l


def leftmost(tetris, x, height):
    lefts = []
    for i in range(height):
        l = tetris[x + i]
        lefts.append(np.where(l == 1)[0][0])
    return min(lefts)


def rightmost(tetris, x, height):
    rights = []
    for i in range(height):
        l = tetris[x + i]
        rights.append(np.where(l == 1)[0][-1])
    return max(rights)


def collides_next(tetris, top, height):
    if top + height >= len(tetris):
        return True
    for i in range(height - 1, -1, -1):
        addition = np.add(tetris[top + i], tetris[top + i + 1])
        print(addition)
        if np.where(addition == 2)[0].size > 0:
            return True
    return False


#    addition = np.add(tetris[bottomx],tetris[bottomx+1])
#    return np.where(addition == 2)[0].size > 0


def drop(tetris, top, height):
    print(top, height)
    for i in range(height - 1, -1, -1):
        tetris[top + i + 1, :] = np.add(tetris[top + i], tetris[top + i + 1])
        tetris[top + i, :] = [0, 0, 0, 0, 0, 0, 0]


n = 0
while n < 10:
    jet = -1
    highest = 0
    for l in tetris:
        print(l)
        if np.any(l):
            print(np.any(l))
            break
        highest +=1
    
    tetris = expand_tetris(tetris,n=3-highest)
    shape = shapes[n % len(shapes)]
    left = 1
    top = 0
    width = 0
    for each_line in shape:
        if len(each_line) > width:
            width = len(each_line)
    height = put(tetris, shape, top, left)
    print("new")
    while top + height < len(tetris):  #not collides_next(tetris,top,height):
        jet += 1
        if jet % 2 == 1:
            if jets[jet%len(jets)] == '>' and left+width <= 6:
                remove(tetris, shape, top, left)
                left += 1
                put(tetris, shape, top, left)
                if np.where(tetris == 2)[0].size > 0:
                    remove(tetris, shape, top, left)
                    left -= 1
                    put(tetris, shape, top, left)
                    continue
            if jets[jet%len(jets)] == '<' and left > 0:
                remove(tetris, shape, top, left)
                left -= 1
                put(tetris, shape, top, left)
                if np.where(tetris == 2)[0].size > 0:
                    remove(tetris, shape, top, left)
                    left += 1
                    put(tetris, shape, top, left)
                    continue
        else:
            remove(tetris, shape, top, left)            
            top += 1
            put(tetris, shape, top,left)
            if np.where(tetris == 2)[0].size > 0:
                remove(tetris, shape, top, left)
                put(tetris, shape, top - 1,left)
                break
        print_tetris(tetris)
        time.sleep(0.5)
        os.system('clear')
    n += 1
