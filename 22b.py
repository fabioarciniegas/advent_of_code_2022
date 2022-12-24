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
            else:
                print(board[i][j], end="")
        print()

def face(pos):
    for f in tls:
#        D(f"{f=} {tls[f]=} {pos=}")
        if pos[0] >= tls[f][0] and pos[0] <= tls[f][0]+49 and pos[1] >= tls[f][1] and pos[1] <= tls[f][1]+49:
            return f
    return None


def move(inst, board, pos, direction):
    if inst == "L":
        return (direction - 1) % 4
    if inst == "R":
        return (direction + 1) % 4
    if direction == 0:
        D("right")
        move_right(inst, board, pos)
    if direction == 1:
        D("going down")
        move_down(inst, board, pos)
    if direction == 2:
        D("left")
        move_left(inst, board, pos)
    if direction == 3:
        D("up")
        move_up(inst, board, pos)
    return direction


def rightmost(pos):  
    return tls[face(pos)][1]+49

def topmost(pos):  
    return tls[face(pos)][0]    

def bottommost(pos):
    return tls[face(pos)][0] + 49

def leftmost(pos):  
    return tls[face(pos)][1]


def targetright(pos):
    # only good for edges
    target = [None,None]
    next_face = { "A" : "B", "B" : "D", "C" : "B",
                  "D" : "B", "E" : "D", "F" : "D" }
    #0 right, 1 down, 2 left, 3 up
    next_dir = { "A" : 0, "B" : 2, "C" : 3,"D" : 2, "E" : 0, "F" : 3 }

    f = face(pos)
    nf = next_face[f]
    nd = next_dir[f]
#    D(f"{f=}, {nf=} {nd=}")
    
    if nd == 0:
        target[0] = pos[0]
        target[1] = tls[nf][1]
    if nd == 2:
        target[0] = topmost(tls[nf])+(topmost(tls[f])+49 - pos[0])
        target[1] = rightmost(tls[nf])
    if nd == 3:
        target[0] = bottommost(tls[nf])
        target[1] = leftmost(tls[nf]) + (pos[0]-topmost(tls[f]))
    return target,nd


def targetleft(pos):
    # only good for edges
    target = [None,None]
    next_face = { "A" : "E", "B" : "A", "C" : "E",
                  "D" : "E", "E" : "A", "F" : "A" }
    #0 right, 1 down, 2 left, 3 up
    next_dir = { "A" : 0, "B" : 2, "C" : 1,"D" : 2, "E" : 0, "F" : 1 }

    f = face(pos)
    nf = next_face[f]
    nd = next_dir[f]
    D(f"{f=}, {nf=} {nd=}")
    
    if nd == 0:
        target[0] = tls[nf][0]
        target[1] = bottommost(tls[nf])-(pos[0]-topmost(tls[f]))
    if nd == 2:
        target[0] = pos[0]
        target[1] = rightmost(tls[nf])
    if nd == 1:
        target[0] = topmost(tls[nf])
        target[1] = leftmost(tls[nf]) + (pos[0]-topmost(tls[f]))
    return target,nd



           
def move_right(inst, board, pos):
    tiles = int(inst)
    R = rightmost(pos)
    L = leftmost(pos)
#    D(f"{R=}")
#    D(f"{L=}")
    while tiles:
        if pos[1] < R and board[pos[0]][pos[1] + 1] == 1:
            pos[1] += 1
        elif pos[1] == R:
            target, nd = targetright(pos)
            if board[target[0]][target[1]] == 1:
                pos[0],pos[1] = target[0], target[1]
            return tiles-1, nd
        tiles -= 1
    return tiles, 0


def move_down(inst, board, pos):
    tiles = int(inst)
    T = topmost(board, pos)
    B = bottommost(board, pos)
    D(f"{T=}")
    D(f"{B=}")
    while tiles:
        if pos[0] < B and board[pos[0] + 1][pos[1]] == 1:
            pos[0] += 1
#            board[pos[0]][pos[1]] = 3
        elif pos[0] == B and board[T][pos[1]] == 1:
            D(f"{pos=}")
            D(f"{tiles=}")
            pos[0] = T


#            board[pos[0]][pos[1]] = 3
        tiles -= 1


def move_left(inst, board, pos):
    tiles = int(inst)
    R = rightmost(board, pos[0])
    L = leftmost(board, pos[0])
    D(f"{R=}")
    D(f"{L=}")

    while tiles:
        if pos[1] > L and board[pos[0]][pos[1] - 1] == 1:
            pos[1] -= 1
#            board[pos[0]][pos[1]] = 3
        elif pos[1] == L and board[pos[0]][R] == 1:
            pos[1] = R


#            board[pos[0]][pos[1]] = 3
        tiles -= 1


def move_up(inst, board, pos):
    tiles = int(inst)
    T = topmost(board, pos[1])
    B = bottommost(board, pos[1])
    while tiles:
        if pos[0] > T and board[pos[0] - 1][pos[1]] == 1:
            pos[0] -= 1
#            board[pos[0]][pos[1]] = 3
        elif pos[0] == T and board[B][pos[1]] == 1:
            pos[0] = B


#            board[pos[0]][pos[1]] = 3
        tiles -= 1


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

move_regexp = "(\d+|[LR])"
instructions = re.findall(move_regexp, instructions_as_line)

# You begin the path in the leftmost open tile of the top row of tiles.
pos = [0, np.where(board[0] == 1)[0][0]]
direction = 0  #0 right, 1 down, 2 left, 3 up

#board[pos[0], pos[1]] = 3

# test right movement
D(targetright((49,99)))
D(targetright((10,99))) # only good on edges
D(targetright((49,149)))
D(targetright((50,99)))
D(targetright((99,99)))
D(targetright((160,49)))


# test left movement
D(targetleft((0,50)))

# pos = [0,97]
# more = 50
# while more:
#     more,d = move_right(more,board,pos)
#     D(f"{pos=},{more=},{d=}")
# D(f"{pos=}")    








exit(2)
D(board.shape)

for inst in instructions:
    D(f"{pos=}{direction=}")
    direction = move(inst, board, pos, direction)
    #print_board(board)
    #print()
D("-==----------")
#print_board(board)

print(f"{password(board,pos,direction)=}")
