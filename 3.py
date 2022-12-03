import numpy as np
import string

f = open("input_3.txt")

alphabet = list(string.ascii_letters)

total = 0
for line in f.readlines():
    compartment_1 = np.zeros(52)
    compartment_2 = np.zeros(52)
    rucksack = line.strip()
    for letter in rucksack[:len(rucksack)//2]:
        compartment_1[alphabet.index(letter)] = 1
    for letter in rucksack[len(rucksack)//2:]:
        compartment_2[alphabet.index(letter)] = 1
    logical_and = np.logical_and(compartment_1, compartment_2)
#    print( alphabet[np.where(logical_and == True)[0][0]])
    priority = np.where(logical_and == True)[0][0] + 1
    total = total + priority

print(total)
