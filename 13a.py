import numpy as np
import json
import re
import ast




f = open("input_13.txt")


def compare(left,right):
    print(left,right)
    ordered = None
    left_e = left
    right_e = right
    if isinstance(left_e,str):
        left_e = ast.literal_eval(left)
    if isinstance(right_e,str):        
        right_e = ast.literal_eval(right)
    i = 0
    if type(left_e) == list and len(left_e) == 0:
        if type(right_e) == list and len(right_e) > 0:
            print("left out of items, so ordered")
            return True
        else:
            return None

    while i in range(len(left_e)) and ordered == None:
        if len(right_e)<=i:
            print("right out items, so NOT ordered")
            return False
        if isinstance(left_e[i],int) and isinstance(right_e[i],int):
            if left_e[i] < right_e[i]:
                print(left_e[i],"<",right_e[i]," so ordered")
                return True
            elif left_e[i] > right_e[i]:
                print(left_e[i],">",right_e[i]," so NOT ordered")                
                return False
            print(left_e[i],"==",right_e[i]," so continue")            
        elif isinstance(left_e[i],list) and isinstance(right_e[i],list):
            ordered = compare(left_e[i],right_e[i])
        elif isinstance(left_e[i],list) and isinstance(right_e[i],int):
            ordered = compare(left_e[i],[right_e[i]])
        elif isinstance(left_e[i],int) and isinstance(right_e[i],list):
            ordered = compare([left_e[i]],right_e[i])
        i += 1

    if i == len(left_e) and i < len(right_e) and ordered == None:
        print("left ran out of items~ so ordered")
        ordered = True

    print(ordered)
    return ordered
#    if isinstance(left_e,list) and isinstance(right_e,list):
#        return len(left_e) <= len(right_e)

        
#     Could also proceed by refining the regexp below but ast is easy
#     reg = "(\d+\,?)"
#     m = re.match(reg,left)
#     elements = m.groups()
    

ordered = []
i = 1

for left in f:
    right = next(f)
    result = compare(left.strip(), right.strip())
    if result:
        ordered.append(i)
    i += 1
    try:
        space = next(f)
    except StopIteration:
        continue

print(ordered)
print(sum(ordered))


