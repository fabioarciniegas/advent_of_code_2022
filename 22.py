# https://www.sciencedirect.com/science/article/abs/pii/S0377221710002973 ?
import math
import numpy as np
import re
import sys
import logging
from logging import debug as D
from logging import warning as W

np.set_printoptions(threshold=np.inf, linewidth=1000)


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


def move(inst, board, pos, direction):
    if inst == "L":
        return (direction - 1) % 4
    if inst == "R":
        return (direction + 1) % 4
    if direction == 0:
        D("right")        
        move_right(inst, board,pos)
    if direction == 1:
        D("going down")
        move_down(inst, board,pos)
    if direction == 2:
        D("left")
        move_left(inst, board,pos)
    if direction == 3:
        D("up")
        move_up(inst, board,pos)
    return direction

def rightmost(board,row): # assume no u shaped maps
    full = np.where(board[row,:] > 0)
    return np.amax(full)

def topmost(board,column): # assume no u shaped maps
    full = np.where(board[:,column] > 0)
    return np.amin(full)

def bottommost(board,column): # assume no c shaped maps
    full = np.where(board[:,column] > 0)
    return np.amax(full)

def leftmost(board,row): # assume no c shaped maps
    full = np.where(board[row,:] > 0)
    return np.amin(full)
    
def move_right(inst, board, pos):
    tiles = int(inst)
    R = rightmost(board,pos[0])
    L = leftmost(board,pos[0])    
    D(f"{R=}")
    D(f"{L=}")
    
    while tiles:
        if pos[1] + 1 <= R and board[pos[0]][pos[1] + 1] == 1:
            pos[1] += 1
            board[pos[0]][pos[1]] = 3
        elif pos[1] == R and board[pos[0]][L] == 1:
            pos[1] = L
            board[pos[0]][pos[1]] = 3
        tiles -= 1

def move_down(inst, board, pos):
    tiles = int(inst)
    T = topmost(board,pos[1])
    B = bottommost(board,pos[1])
    while tiles:
        if pos[0] + 1 <= B and board[pos[0]+1][pos[1]] == 1:
            pos[0] += 1
            board[pos[0]][pos[1]] = 3
        elif pos[0] == B and board[T][pos[1]] == 1:
            pos[0] = T
            board[pos[0]][pos[1]] = 3
        tiles -= 1

def move_left(inst, board, pos):
    tiles = int(inst)
    R = rightmost(board,pos[0])
    L = leftmost(board,pos[0])    
    D(f"{R=}")
    D(f"{L=}")
    
    while tiles:
        if pos[1] - 1 <= L and board[pos[0]][pos[1] - 1] == 1:
            pos[1] -= 1
            board[pos[0]][pos[1]] = 3
        elif pos[1] == L and board[pos[0]][R] == 1:
            pos[1] = R
            board[pos[0]][pos[1]] = 3
        tiles -= 1

def move_up(inst, board, pos):
    tiles = int(inst)
    T = topmost(board,pos[1])
    B = bottommost(board,pos[1])
    while tiles:
        if pos[0] - 1 <= T and board[pos[0]-1][pos[1]] == 1:
            pos[0] -= 1
            board[pos[0]][pos[1]] = 3
        elif pos[0] == T and board[B][pos[1]] == 1:
            pos[0] = B
            board[pos[0]][pos[1]] = 3
        tiles -= 1

def password(board,pos,direction):
    return (pos[0]*1000)+(pos[1]*4)+direction


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

board[pos[0], pos[1]] = 3

D(board.shape)

for inst in instructions:
    direction = move(inst, board, pos, direction)
    print_board(board)
    print()

print(f"{password(board,pos,dir)=}")
    

    
