import math
import numpy as np
import re
import sys
import logging
from logging import debug as D
from logging import warning as W

np.set_printoptions(threshold=np.inf, linewidth=1000)

offset_h = 0
offset_v = 0

def read_input(filename):
    f = open(filename)
    length = 0
    height = 0
    for l in f:
        if l == "\n":
            break
        length = max(len(l), length)
        height += 1

    offset_h = height
    offset_v = length
        
    # drake_meme(calculate dynamically, overprovision)
    board = np.zeros((height*3, length*3), dtype=int)

    f = open(filename)
    i = 0
    for l in f:
        l = l[0:len(l)]
        j = 0
        for c in l:
            if c == "#":
                board[i+offset_v][j+offset_h] = 2
            elif c == ".":
                board[i+offset_v][j+offset_h] = 0
            j += 1
        i += 1
    return board


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


def bounding_rect(board):
    left = min([leftmost(board,x) for x in range(board.shape[0])])
    right = max([rightmost(board,x) for x in range(board.shape[0])])
    top = min([topmost(board,x) for x in range(board.shape[1])])
    bottom = max([bottommost(board,x) for x in range(board.shape[1])])
    D(f"Bounding box {top=} {left=} {bottom=} {right=}")
    return left,right,top,bottom

#TODO: move to a more elegant matrix/convolution based approach if time permits
def check_neighbors(board,i,j):
    n = {}
    n["NW"] = board[i-1][j-1]
    n["N"]  = board[i-1][j]
    n["NE"] = board[i-1][j+1]
    n["W"] =  board[i][j-1]
    n["E"] =  board[i][j+1]
    n["SW"] = board[i+1][j-1]    
    n["S"] = board[i+1][j]
    n["SE"] = board[i+1][j+1]
    return max([ n[x] for x in n]) == 0,n

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

# TODO: changes these helper functions,which are not the most idiomatic for numpy
# just legacy from tetris problem (22)
def rightmost(board,row): 
    full = np.where(board[row,:] > 0)
    return np.amax(full) if len(full[0]) else -math.inf

def topmost(board,column): # assume no u shaped maps
    full = np.where(board[:,column] > 0)
    return np.amin(full) if len(full[0]) else math.inf

def bottommost(board,column): # assume no c shaped maps
    full = np.where(board[:,column] > 0)
    return np.amax(full) if len(full[0]) else -math.inf

def leftmost(board,row): # assume no c shaped maps
    full = np.where(board[row,:] > 0)
    return np.amin(full) if len(full[0]) else math.inf
    
def move_right(inst, board, pos):
    tiles = int(inst)
    R = rightmost(board,pos[0])
    L = leftmost(board,pos[0])    
    D(f"{R=}")
    D(f"{L=}")
    
    while tiles:
        if pos[1] < R and board[pos[0]][pos[1] + 1] == 1:
            pos[1] += 1
#            board[pos[0]][pos[1]] = 3
        elif pos[1] == R and board[pos[0]][L] == 1:
            pos[1] = L
#            board[pos[0]][pos[1]] = 3
        tiles -= 1

def move_down(inst, board, pos):
    tiles = int(inst)
    T = topmost(board,pos[1])
    B = bottommost(board,pos[1])
    D(f"{T=}")
    D(f"{B=}")
    while tiles:
        if pos[0] < B and board[pos[0]+1][pos[1]] == 1:
            D(f"{pos=}")
            D(f"{tiles=}")
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
    R = rightmost(board,pos[0])
    L = leftmost(board,pos[0])    
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
    T = topmost(board,pos[1])
    B = bottommost(board,pos[1])
    while tiles:
        if pos[0] > T and board[pos[0]-1][pos[1]] == 1:
            pos[0] -= 1
#            board[pos[0]][pos[1]] = 3
        elif pos[0] == T and board[B][pos[1]] == 1:
            pos[0] = B
#            board[pos[0]][pos[1]] = 3
        tiles -= 1


filename = ""
if len(sys.argv) > 1:
    filename = sys.argv[1]
    if len(sys.argv) > 2 and sys.argv[2] == "--debug":
        logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    else:
        logging.basicConfig(stream=sys.stderr, level=logging.WARNING)
else:
    print("usage: python 24.py <filename>")

board = read_input(filename)

print_board(board)
bounding_rect(board)



for rounds in range(10):
    l,r,t,b = bounding_rect(board)
    for i in range(t,b):
        for j in range(l,r):
            alone, n = check_neighbors(board,i,j)
            if alone:
                D(f"Elf alone at {i=} {j=}")
            elif n["NW"] == 0 and n["N"] == 0 and n["NE"] and active_rule == 0:
                D(f"Elf proposing to move north from {i=} {j=}")
                board[i-1][j]=2
            elif n["SW"] == 0 and n["S"] == 0 and n["SE"] and active_rule == 1:
                D(f"Elf proposing to move south from {i=} {j=}")
                board[i+1][j]=2
            elif n["W"] == 0 and n["NW"] == 0 and n["SW"] and active_rule == 2:
                D(f"Elf proposing to move north from {i=} {j=}")
                board[i][j-1]=2
            elif n["E"] == 0 and n["NE"] == 0 and n["SE"] and active_rule == 0:
                D(f"Elf proposing to move north from {i=} {j=}")
                board[i][j+1]=2
                
exit(2)


    

