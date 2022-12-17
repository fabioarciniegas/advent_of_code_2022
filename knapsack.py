import numpy as np
np.set_printoptions(threshold=np.inf, linewidth=1000)

# each item has a value and a size (e.g. dollars, weight)
items = [[3, 4], [2, 3], [4, 2], [4, 3]]

capacity = 6

def knapsack(capacity, items):
    solutions = np.zeros((len(items)+1, capacity+1))
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
    return solutions[len(items)][capacity], solutions


def reconstruct_knapsack(A,items,capacity):
    S = []
    c = capacity
    for i in range(len(items),0,-1):
        s_i = items[i-1][1]
        v_i = items[i-1][0]
#        print(i-1,v_i,s_i)
        if s_i <= c and A[i][c - s_i] + v_i >= A[i][c]:
            S.append(i-1)
            c = c - s_i
    return S



x,solutions = knapsack(capacity, items)

print(items)
print(x)
print(solutions)
print(reconstruct_knapsack(solutions,items,capacity))


items = [
    [0,0],
    [13,2],
    [0,2],
    [2,3],
    [21,3],
    [20,2],
    [3,4],
    [0,5],
    [0,5],
    [22,6]
]

capacity = 10
x,solutions = knapsack(10, items)

print(items)
print(x)
print(solutions)
print(reconstruct_knapsack(solutions,items,capacity))


        
