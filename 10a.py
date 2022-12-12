f = open("input_10.txt")

done = False
state = 0
X = 1
cycle = 0
cycle_of_interest = 20
signals = []
op = ""
amt = 0

while done is not True:
    # 0 ready to read next instruction
    # 1 middle of an add
    cycle = cycle + 1
    print(cycle,X)
    if cycle == cycle_of_interest:
        signals.append(cycle * X)
        cycle_of_interest = cycle_of_interest + 40
    if state == 1:
        X = X + int(amt)
        state = 0
        continue
    if state == 0:
        try:
            inst = next(f)
        except StopIteration:
            done = True
            continue
        op = inst[0:4]
        amt = inst[4:]
        if op == "noop":
            continue
        if op == "addx":
            state = 1

print(sum(signals))
