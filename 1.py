f = open("input_1.txt")
max = 0
max_1 = 0
max_2 = 0

count = 0
for line in f.readlines():
    l = line.strip()
    if l == "":
        if count > max:
            max_2 = max_1
            max_1 = max
            max = count
        elif count > max_1:
            max_2 = max_1
            max_1 = count
        elif count > max_2:
            max_2 = count
        count = 0
    else:
        count = count + int(l)
print(max+max_1+max_2)
