import numpy as np
import sys
import logging
from logging import debug as D
import cv2

np.set_printoptions(threshold=np.inf, linewidth=1000)

BU, BD, BL, BR, GR, WL, P = "^", "v", "<", ">", ".", "#", "O"
enc, dec, col = {}, {}, {}
enc[BU],enc[BD],enc[BL],enc[BR],enc[GR],enc[WL], enc[P] = 1,2,3,4,5,6,7
dec = {v: k for k, v in enc.items()}

col[BU] = col[BD] = col[BL] = col[BR] = 90
col[P], col[GR], col[WL] = 255, 0, 100


def read_input(filename):
    f = open(filename)
    lines = []
    length = 0
    height = 0
    for l in f:
        length = max(len(l), length)
        height += 1
        lines.append(l)

    board = np.zeros((height-2, length-3), dtype=int) # no walls

    f = open(filename)
    i = 0 #TODO: simplify all non-idiomatic loops
    for l in lines[1:-1]:
        l = l[0:len(l)-1]
        j = 0
        for c in l[1:-1]:
            board[i][j] = enc[c]
            j += 1
        i += 1
    return board

def print_board(board,sequence=0):
    pic = np.zeros((board.shape[0],board.shape[1]),dtype=int)
    for i in range(len(board)):
        for j in range(len(board[i])):
            print(dec[board[i][j]],end="")
            pic[i][j] = col[dec[board[i][j]]]
        print()
        cv2.imwrite(f"24_{sequence:05}.png",pic)

def out_of_bounds(board,i,j):
    return i >= board.shape[0] or i < 0 or  j >= board.shape[1] or j < 0


def solve(board, start, goal, step):
    height = board.shape[0]
    width = board.shape[1]
    options = set([start])
    while True:
        next_options = set()
        for p in options:

            for i,j in [ p, (p[0]-1,p[1]), (p[0]+1,p[1]),(p[0],p[1]-1), (p[0],p[1]+1)]:
                if (i,j) == goal:
                    return step
                if out_of_bounds(board,i,j):
                    D(f"{i=},{j=} out of bounds")
                    continue
                # at step n the right-moving blizzard '>' that was at
                # position j-n at the start will be at j.
                # credit to @ViliamPuck for this insight.
                free = \
                    board[i][(j-step) % width] != enc[BR] and \
                    board[i][(j+step) % width] != enc[BL] and \
                    board[(i-step)%height][j] != enc[BD] and \
                    board[(i+step)%height][j] != enc[BU]                         
                if free:
                    next_options.add((i,j))
            options = next_options
            if not options:
                options.add(start)
        step += 1
    #        if step < 1000:
    #            print_board(board,step)

filename = ""
if len(sys.argv) > 1:
    filename = sys.argv[1]
    if len(sys.argv) > 2 and sys.argv[2] == "--debug":
        logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    else:
        logging.basicConfig(stream=sys.stderr, level=logging.WARNING)
else:
    print("usage: python 25.py <filename>")

board = read_input(filename)
print_board(board)


print(solve(board,(-1, 0), (board.shape[0], board.shape[1] - 1), 1))
#print(solve(start, goal, solve(goal, start, s1)))
