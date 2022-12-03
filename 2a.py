f = open("input_2.txt")

# A rock, B paper, C Scissors
# X rock, Y paper, Z Scissors

def win(r):
    if r == ["A","Y"] or r == ["B","Z"] or r == ["C","X"]:
        return 6
    if r == ["A","X"] or r == ["B","Y"] or r == ["C","Z"]:
        return 3
    return 0

def sel(p):
    if p == "X":
        return 1
    if p == "Y":
        return 2
    if p == "Z":
        return 3

total = 0
for l in f.readlines():
    r = l.split()
    win_score = win(r)
    sel_score = sel(r[1])
    total = total + win_score + sel_score

print(total)
