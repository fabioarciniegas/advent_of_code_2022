f = open("input_2.txt")

# A rock, B paper, C Scissors
# X rock, Y paper, Z Scissors

win_scores = {"A Y": 6, "B Z": 6, "C X": 6, "A X": 3, "B Y": 3, "C Z": 3}
sel_scores = {"X": 1, "Y": 2, "Z": 3}


def win_points(r):
    return win_scores.get(r[0] + " " + r[1], 0)


def selection_points(r_1):
    return sel_scores[r_1]


clues = {
    "X": {"A": "Z", "B": "X", "C": "Y" },
    "Y": {"A": "X", "B": "Y", "C": "Z" },
    "Z": {"A": "Y", "B": "Z", "C": "X" }
}


def answer(opp, clue):
    return clues[clue][opp]


total = 0

for l in f.readlines():
    r = l.split()
    r[1] = answer(r[0], r[1])
    total = total + win_points(r) + selection_points(r[1])

print(total)
