import numpy as np
import json
import re
import ast


f = open("input_13.txt")
#f = open("input_sample_13.txt")




def compare(left,right):
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
            return True
        else:
            return None

    while i in range(len(left_e)) and ordered == None:
        if len(right_e)<=i:
            return False
        if isinstance(left_e[i],int) and isinstance(right_e[i],int):
            if left_e[i] < right_e[i]:
                return True
            elif left_e[i] > right_e[i]:
                return False
        elif isinstance(left_e[i],list) and isinstance(right_e[i],list):
            ordered = compare(left_e[i],right_e[i])
        elif isinstance(left_e[i],list) and isinstance(right_e[i],int):
            ordered = compare(left_e[i],[right_e[i]])
        elif isinstance(left_e[i],int) and isinstance(right_e[i],list):
            ordered = compare([left_e[i]],right_e[i])
        i += 1

    if i == len(left_e) and i < len(right_e) and ordered == None:
        ordered = True

    return ordered

ordered = []
i = 1

all = ["2","6"]

for left in f:
    right = next(f)
    result = compare(left.strip(), right.strip())
    if result:
        ordered.append(i)
    i += 1
    left = left.strip()
    while '[]' in left:
        left = left.replace('[]','')
    left = left.replace(',','')
    left = left.replace(']','')
    left = left.replace('[','')    

    right = right.strip()    
    while '[]' in right:
        right = right.replace('[]','')
    right = right.replace(',','')
    right = right.replace(']','')
    right = right.replace('[','')

    all.append(left)
    all.append(right)
    try:
        space = next(f)
    except StopIteration:
        continue

all.sort()
marker1 = None
marker2 = None

for i in range(len(all)):
    print(all[i])
    if marker1 == None and len(all[i])>0 and all[i] == '2':
        marker1 = i
    if marker2 == None and len(all[i])>0 and all[i] == '6':
        marker2 = i

#16072 too low
#28776
# 1-based count
marker1 +=1
marker2 +=1
print(marker1,marker2,marker1*marker2)
