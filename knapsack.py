import numpy as np

# each item has a value and a size (e.g. dollars, weight)
items = [[3, 4], [2, 3], [4, 2], [4, 3]]

capacity = 6
solutions = np.zeros((len(items)+1, capacity+1))


def knapsack(solutions, capacity, items):
    # base case of i=0
    for c in range(capacity):
        solutions[0][c] = 0
    for i in range(1, len(items)+1):
        s_i = items[i-1][1]
        v_i = items[i-1][0]     
        for c in range(capacity+1):
            if s_i > c:
                solutions[i][c] = solutions[i - 1][c]
            else:
                solutions[i][c] = max(solutions[i - 1][c],
                                      solutions[i - 1][c - s_i] + v_i)
    return solutions[len(items)][capacity]


x = knapsack(solutions, capacity, items)

print(x)
print(solutions)
