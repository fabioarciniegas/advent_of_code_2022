import numpy as np
import os
import sys
import time

np.set_printoptions(threshold=np.inf, linewidth=1000)

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


def shape_width(shape):
    width = 0  # TODO: replace with a numpy idiomatic way
    for each_line in shape:
        if len(each_line) > width:
            width = len(each_line)
    return width


def determine_period(tetris):
    period = 0
    s = len(tetris) // 2  # assume the line in the middle is already periodic
    p = 1
    while period == 0:
        for i in range(p + 1):
            if not (tetris[s + i] == tetris[s + i + p]).all():
                p += 1
                break
            if i == p and period < p:
                period = p
    return period


def determine_prologue(tetris, period):
    prologue = 0
    s = len(tetris) - 1
    pl = 0
    while prologue == 0:
        for i in range(1, period + 1):
            if not (tetris[s - pl - i] == tetris[s - pl - i - period]).all():
                pl += 1
                break
            if i == period:
                prologue = pl
    return prologue


def read_jets(filename):
    f = open(filename)
    jets = f.readline()
    jets = jets.strip()
    return jets


def put_n_shapes(tetris,
                 jets,
                 goal,
                 mode,
                 lines_in_prologue=-1,
                 lines_in_period=-1,
                 jet=0):
    n = 0
    blocks_in_prologue = -1
    blocks_in_period = -1
    jet_at_n_minus_1 = -1
    while n < goal:
        highest = first_non_empty(tetris)
        shape = shapes[n % len(shapes)]
        left = 2
        width = shape_width(shape)
        height = len(shape)
        jet_at_n_minus_1 = jet

        top = highest - 3 - height  # start next shape 3 drom the highest
        #    print(highest,top)

        if top < 0:
            tetris = expand_tetris(tetris, -top)
            top = 0

        put(tetris, shape, top, left)

        jetted = True
        while True:

            if jetted:  #alternate between falling and jetting
                if jets[jet] == '>' and left + width <= 6:
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
                jet = jet % len(jets)

            else:
                if top + height >= len(tetris):  # bottom
                    break
                remove(tetris, shape, top, left)
                top += 1
                put(tetris, shape, top, left)
                if np.where(tetris == 2)[0].size > 0:
                    remove(tetris, shape, top, left)
                    put(tetris, shape, top - 1, left)
                    break
            jetted = not jetted

            if mode == "animate":
                print_tetris(tetris)
                time.sleep(0.6)
                os.system('clear')

            if mode == "cached":
                if blocks_in_prologue == -1 and tower_height(
                        tetris) > lines_in_prologue:
                    blocks_in_prologue = n 

                if blocks_in_period == -1 and tower_height(
                        tetris) > lines_in_prologue + lines_in_period:
                    blocks_in_period = n - blocks_in_prologue + 1

                if blocks_in_period > 0 and blocks_in_prologue > 0:
#                    print("blocks in prologue and period:",blocks_in_prologue,blocks_in_period)
                    periodic_chunks = (goal -
                                       blocks_in_prologue) // blocks_in_period
                    lines_in_periodic_chunks = periodic_chunks * lines_in_period
                    blocks_out_of_prologue_and_chunks = (
                        goal - blocks_in_prologue) % blocks_in_period
                    return blocks_in_prologue,periodic_chunks, lines_in_periodic_chunks, blocks_out_of_prologue_and_chunks, jet_at_n_minus_1

        n += 1
    if mode == "print":
        print_tetris(tetris)

    if mode == "height":
        print(tower_height(tetris))
        return tower_height(tetris)


def read_cached(filename, tetris):
    f = open(filename)
    lines = []
    for l in f:
        l = l.strip()
        if l == ".......":
            continue
        as_zeros = [0 if c == '.' else 1 for c in l]
        tetris = np.append(tetris, [as_zeros], axis=0)
    return tetris


goal = 100
mode = "animate"
tetris = np.ones((0, 7), dtype=int)
jets = []
cached_file = ""

if len(sys.argv) > 1:
    mode = sys.argv[1]
    goal = int(sys.argv[2])
    jets = read_jets(sys.argv[3])
    if len(sys.argv) > 4:
        cached_file = sys.argv[4]
else:
    print(
        "Usage: python 17 [height|print|animate|cached] <number of blocks> <input file> <cached print file>"
    )
    print(
        "To ease testing in part 2, the preferred usage is to first do a print and save to a cached file, then use that as basis for part 2. see 17.sh"
    )
    exit(1)

if mode != "cached":
    put_n_shapes(tetris, jets, goal, mode)

if mode == "cached":
    tetris = read_cached(cached_file, tetris)
#    print(tower_height(tetris))

    lines_in_period = determine_period(tetris)
    lines_in_prologue = determine_prologue(tetris, lines_in_period)
#    print("lines in prologue and period:",lines_in_prologue, lines_in_period)

    fresh = np.ones((0, 7), dtype=int)
    blocks_in_prologue,periodic_chunks, lines_in_periodic_chunks, blocks_out_of_prologue_and_chunks, jet_at_n_minus_1 = put_n_shapes(
        fresh, jets, goal, mode, lines_in_prologue, lines_in_period)

#    print(blocks_in_prologue, periodic_chunks, lines_in_periodic_chunks, blocks_out_of_prologue_and_chunks, jet_at_n_minus_1)


    fresh = np.ones((0, 7), dtype=int)
    print(lines_in_periodic_chunks + put_n_shapes(fresh, jets, blocks_in_prologue+blocks_out_of_prologue_and_chunks, "height"))

        
    exit(0)

    # right answer part 2:1541449275365
