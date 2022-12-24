# https://www.sciencedirect.com/science/article/abs/pii/S0377221710002973 ?
import math
import numpy as np
import re
import sys
import logging
from logging import debug as D
from logging import warning as W

np.set_printoptions(threshold=np.inf, linewidth=1000)

tls = {
    'A': [0, 50],
    'B': [0, 100],
    'C': [50, 50],
    'D': [100, 50],
    'E': [100, 0],
    'F': [150, 0]
}


def read_input(filename):
    targets = {}
    f = open(filename)
    length = 0
    height = 0
    for l in f:
        if l == "\n":
            break
        length = max(len(l), length)
        height += 1

    board = np.zeros((height, length), dtype=int)
    f = open(filename)
    instructions = ""
    f.close()
    f = open(filename)

    i = 0
    for l in f:
        l = l[0:len(l)]
        if l == "\n":
            instructions = next(f)
            break
        j = 0
        for c in l:
            if c == "#":
                board[i][j] = 2
            elif c == ".":
                board[i][j] = 1
            j += 1
        i += 1

    return board, instructions


def print_board(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 0:
                print(" ", end="")
            elif board[i][j] == 1:
                print(".", end="")
            elif board[i][j] == 2:
                print("#", end="")
            elif board[i][j] == -3:
                print(">", end="")
            elif board[i][j] == -4:
                print("v", end="")
            elif board[i][j] == -5:
                print("<", end="")
            elif board[i][j] == -6:
                print("^", end="")
            else:
                print(board[i][j], end="")
        print()


def face(pos):
    for f in tls:
        #        D(f"{f=} {tls[f]=} {pos=}")
        if pos[0] >= tls[f][0] and pos[0] <= tls[f][0] + 49 and pos[1] >= tls[
                f][1] and pos[1] <= tls[f][1] + 49:
            return f
    return None


def rightmost(pos):
    return tls[face(pos)][1] + 49


def topmost(pos):
    return tls[face(pos)][0]


def bottommost(pos):
    return tls[face(pos)][0] + 49


def leftmost(pos):
    return tls[face(pos)][1]


def trace(pos, d):
    dir_codes = {0: -3, 1: -4, 2: -5, 3: -6}
    board_viz[pos[0]][pos[1]] = dir_codes[d]


def targetright(pos):
    target = [None, None]
    next_face = {"A": "B", "B": "D", "C": "B", "D": "B", "E": "D", "F": "D"}
    # 0 right, 1 down, 2 left, 3 up
    next_dir = {"A": 0, "B": 2, "C": 3, "D": 2, "E": 0, "F": 3}

    f = face(pos)
    nf = next_face[f]
    nd = next_dir[f]
    D(f"{pos=} {f=}, {nf=} {nd=}")

    if nd == 0:
        target[0] = topmost(tls[nf]) + (pos[0]- topmost(tls[f]))
        target[1] = leftmost(tls[nf])
    if nd == 2:
        target[0] = topmost(tls[nf]) + (pos[0] - topmost(tls[f]))
        target[1] = rightmost(tls[nf])
    if nd == 3:
        target[0] = bottommost(tls[nf])
        target[1] = leftmost(tls[nf]) + (pos[0] - topmost(tls[f]))
    return target, nd


def targetleft(pos):
    # only good for edges
    target = [None, None]
    next_face = {"A": "E", "B": "A", "C": "E", "D": "E", "E": "A", "F": "A"}
    next_dir = {"A": 0, "B": 2, "C": 1, "D": 2, "E": 0, "F": 1}

    f = face(pos)
    nf = next_face[f]
    nd = next_dir[f]
    D(f"{pos=} {f=}, {nf=} {nd=}")

    if nd == 0:
        target[0] = topmost(tls[nf]) + (pos[0]- topmost(tls[f]))
        target[1] = leftmost(tls[nf])
    if nd == 2:
        target[0] = topmost(tls[nf]) + (pos[0]- topmost(tls[f]))
        target[1] = rightmost(tls[nf])
    if nd == 1:
        target[0] = topmost(tls[nf])
        target[1] = leftmost(tls[nf]) + (pos[0] - topmost(tls[f]))
    return target, nd


def targetdown(pos):
    # only good for edges
    target = [None, None]
    next_face = {"A": "C", "B": "C", "C": "D", "D": "F", "E": "F", "F": "B"}
    next_dir = {"A": 1, "B": 2, "C": 1, "D": 2, "E": 1, "F": 1}

    f = face(pos)
    nf = next_face[f]
    nd = next_dir[f]
    D(f"{pos=} {f=}, {nf=} {nd=}")

    if nd == 1:
        target[0] = topmost(tls[nf])
        target[1] = leftmost(tls[nf]) + (pos[1] - leftmost(tls[f]))
    if nd == 2:
        target[0] = topmost(tls[nf]) + (pos[1] - leftmost(tls[f]))
        target[1] = rightmost(tls[nf])
    return target, nd


def targetup(pos):
    # only good for edges
    target = [None, None]
    next_face = {"A": "F", "B": "F", "C": "A", "D": "C", "E": "C", "F": "E"}
    next_dir = {"A": 0, "B": 3, "C": 3, "D": 3, "E": 0, "F": 3}

    f = face(pos)
    nf = next_face[f]
    nd = next_dir[f]
    D(f"{f=}, {nf=} {nd=}")

    if nd == 0:
        target[0] = topmost(tls[nf]) + (pos[1] - leftmost(tls[f]))
        target[1] = leftmost(tls[nf])
    if nd == 3:
        target[0] = bottommost(tls[nf])
        target[1] = leftmost(tls[nf]) + (pos[1] - leftmost(tls[f]))
    return target, nd


def manual_test_cases():
    # coarse minimal testing
    D(targetright((49, 99)))
    D(targetright((49, 149)))
    D(targetright((50, 99)))
    D(targetright((99, 99)))
    D(targetright((160, 49)))
    D(targetleft((0, 50)))
    ops = targetleft, targetdown, targetright, targetup
    for corner in tls.values():
        for op in ops:
            print(f"{corner} using {op.__name__} : {op(corner)}")


def move_right(inst, board, pos):
    tiles = int(inst)
    R = rightmost(pos)
    while tiles:
        if pos[1] < R and board[pos[0]][pos[1] + 1] == 1:
            pos[1] += 1
            trace(pos,0)
        elif pos[1] == R:
            target, nd = targetright(pos)
            if board[target[0]][target[1]] == 1:
                pos[0], pos[1] = target[0], target[1]
                trace(pos,nd)
            return tiles - 1, nd
        tiles -= 1
    return tiles, 0


def move_down(inst, board, pos):
    tiles = int(inst)
    B = bottommost(pos)
    while tiles:
        if pos[0] < B and board[pos[0] + 1][pos[1]] == 1:
            pos[0] += 1
            trace(pos,1)
        elif pos[0] == B:
            D(f"ON the bottommost:{pos=}")
            target, nd = targetdown(pos)
            D(f"so {target=} {nd=} {pos=}")            
            if board[target[0]][target[1]] == 1:
                pos[0], pos[1] = target[0], target[1]
                trace(pos,nd)
            return tiles - 1, nd
        tiles -= 1
    return tiles, 1


def move_left(inst, board, pos):
    tiles = int(inst)
    L = leftmost(pos)
    while tiles:
        if pos[1] > L and board[pos[0]][pos[1] - 1] == 1:
            pos[1] -= 1
            trace(pos,2)
        elif pos[1] == L:
            target, nd = targetleft(pos)
            if board[target[0]][target[1]] == 1:
                pos[0], pos[1] = target[0], target[1]
                trace(pos,nd)
            return tiles - 1, nd
        tiles -= 1
    return tiles, 2


def move_up(inst, board, pos):
    tiles = int(inst)
    T = topmost(pos)
    while tiles:
        if pos[0] > T and board[pos[0] - 1][pos[1]] == 1:
            pos[0] -= 1
            trace(pos,3)
        elif pos[0] == T:
            target, nd = targetup(pos)
            if board[target[0]][target[1]] == 1:
                pos[0], pos[1] = target[0], target[1]
                trace(pos,nd)
            return tiles - 1, nd
        tiles -= 1
    return tiles, 3


def move(inst, board, pos, direction):
    #0 right, 1 down, 2 left, 3 up
    if inst == "L":
        nd = { 0:3 , 1:0, 2:1, 3:2}
        return nd[direction]
    elif inst == "R":
        nd = { 0:1 , 1:2, 2:3, 3:0}
        return nd[direction]

    tiles = int(inst)
    while tiles:
        if direction == 0:
            tiles, direction = move_right(tiles, board, pos)
        if direction == 1:
            tiles, direction = move_down(tiles, board, pos)
        if direction == 2:
            tiles, direction = move_left(tiles, board, pos)
        if direction == 3:
            tiles, direction = move_up(tiles, board, pos)
    return direction


def password(board, pos, direction):
    return ((pos[0] + 1) * 1000) + ((pos[1] + 1) * 4) + direction


filename = ""
if len(sys.argv) > 1:
    filename = sys.argv[1]
    if len(sys.argv) > 2 and sys.argv[2] == "--debug":
        logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    else:
        logging.basicConfig(stream=sys.stderr, level=logging.WARNING)
else:
    print("usage: python 22.py <filename>")

board, instructions_as_line = read_input(filename)

board_viz,_ = read_input(filename)#('U1',1))

move_regexp = "(\d+|[LR])"
instructions = re.findall(move_regexp, instructions_as_line)

# You begin the path in the leftmost open tile of the top row of tiles.
pos = [0, np.where(board[0] == 1)[0][0]]
direction = 0  #0 right, 1 down, 2 left, 3 up

for inst in instructions:
    D(f"{pos=}{direction=}")
    direction = move(inst, board, pos, direction)

print_board(board_viz)
print(f"{pos=} {direction=} {password(board,pos,direction)=}")


exit(0)

#149400 too high
#150062
#89316 too low
#71231


# 10R200L10R200L10R10L200R10L5L200
