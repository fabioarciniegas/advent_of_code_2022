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
        length = max(len(l),length)
        height +=1

    board = np.zeros((height,length),dtype=int)
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
                board[i][j] = -1
            elif c == ".":
                board[i][j] = 1
            j += 1
        i += 1

    return board, instructions

def print_board(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 0:
                print(" ",end="")
            elif board[i][j] == 1:
                print(".",end="")
            elif board[i][j] == -1:
                print("#",end="")
            else:
                print(board[i][j],end="")
                
        print()


def move(inst,board,pos,dir):
    if inst == "L":
        return (dir - 1)%4
    if inst == "R":
        return (dir + 1)%4
    if dir == 1:
        move_right(inst,board)

def move_right(inst,board,pos):
    tiles = int(inst)
    while tiles:
        if board[pos[0][[pos[1]+1] == -1 or (pos[1]+1 == len(board[pos[0]]) and board[pos[0]][0] == -1):
            return pos
        if board[pos[0]][pos[1]+1] >= 0:
            pos[1] +=1
        if pos[1]+1 == len(board[pos[0]]):
            pos[1] = 0
        tiles -= 1
        

    

filename = ""
if len(sys.argv) > 1:
    filename = sys.argv[1]
    if len(sys.argv) > 2 and sys.argv[2] == "--debug":
        logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    else:
        logging.basicConfig(stream=sys.stderr, level=logging.WARNING)
else:
    print("usage: python 22.py <filename>")

board,instructions_as_line = read_input(filename)

move = "(\d+|[LR])"
instructions = re.findall(move,instructions_as_line)

# You begin the path in the leftmost open tile of the top row of tiles.
pos = [0,np.where(board[0] == 1)[0][0]]
dir = 0 #0 right, 1 down, 2 left, 3 up

board[pos[0],pos[1]] = 2

print_board(board)


for inst in instructions:
    dir = move(inst,board,pos,dir)
