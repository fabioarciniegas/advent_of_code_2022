import numpy as np
import string

f = open("input_3.txt")

alphabet = list(string.ascii_letters)

total = 0
for line in f:
    elfa = line.strip()
    elfb = next(f).strip()
    elfc = next(f).strip()
    rucksack_1 = np.zeros(52)
    rucksack_2 = np.zeros(52)
    rucksack_3 = np.zeros(52)
    for letter in elfa:
        rucksack_1[alphabet.index(letter)] = 1
    for letter in elfb:
        rucksack_2[alphabet.index(letter)] = 1
    for letter in elfc:
        rucksack_3[alphabet.index(letter)] = 1
    logical_and = np.logical_and(np.logical_and(rucksack_1, rucksack_2),
                                 rucksack_3)
    priority = np.where(logical_and == True)[0][0] + 1
    total = total + priority

print(total)
