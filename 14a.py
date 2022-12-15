import numpy as np
import re
from PIL import Image
import cv2

f = open("input_14_sample.txt")
f = open("input_14.txt")




cart = np.zeros((900,900),dtype=int)

ROCK = 200
SAND = 100

segments = "(\d+),(\d+)"

def rockline(cart,x1,y1,x2,y2):
    cart[x1][y1] = ROCK
    if x2 > x1:
        rockline(cart,x1+1,y1,x2,y2)
    if y2 > y1:
        rockline(cart,x1,y1+1,x2,y2)
        

for l in f:
#    print(l)
    m = re.findall(segments,l)
#    print(m)
    x1 = int(m[0][0])
    y1 = int(m[0][1])
    for seg in m[1:]:
        x2 = int(seg[0])
        y2 = int(seg[1])
#        print(x1,y1,",", x2,y2)
        rockline(cart,min(x1,x2),min(y1,y2),max(x1,x2),max(y1,y2))
        x1 = x2
        y1 = y2

nz = np.nonzero(cart)
minx = min(nz[0])
maxx = max(nz[0])
miny = 0
maxy = max(nz[1])
#print(minx,maxx,miny,maxy)
# rockline(cart,minx,miny,maxx,miny)
# rockline(cart,maxx,miny,maxx,maxy)
# rockline(cart,minx,maxy,maxx,maxy)
# rockline(cart,minx,miny,minx,maxy)
#rockline(cart,maxx,miny,maxx,maxy)
#rockline(cart,maxx,maxy,minx,miny)    
#    rockline(cart,maxx,miny,maxx,maxy)
#    rockline(cart,maxx,maxy,maxx,miny)
#    rockline(cart,maxx,miny,minx,miny)        


cart[500][0] = 0

def fall(cart,x,y):
    placed = False
    if y > maxy:
        return False
#    if cart[x][y] == SAND and x== 500 and y==0:
#        return False
    if cart[x][y+1] == 0:
        return fall(cart,x,y+1)
    if cart[x-1][y+1] == 0:    
        return fall(cart,x-1,y+1)
    if cart[x+1][y+1] == 0:    
        return fall(cart,x+1,y+1)
    cart[x][y] = SAND
        
    return True
    
    
    # placed = False
    # if cart[x][y] == SAND and x== 500 and y==0:
    #     return False
    # if cart[x][y+1] == SAND:
    #     if cart[x+1][y+1] == 0:
    #         cart[x+1][y+1] = SAND
    #         return True
    #     elif cart[x-1][y+1] == 0:
    #         cart[x-1][y+1] = SAND
    #         return True
    #     else:
    #         cart[x][y] = SAND
    #         return True
    # if cart[x][y+1] == 0:
    #     return fall(cart,x,y+1)
    # if cart[x][y+1] == ROCK:
    #     cart[x][y] = SAND
    #     return True


placed = True
grains = 0
while placed:
    grains +=1
    placed = fall(cart,500,0)
    if grains % 100:
        pic = cart[minx-1:maxx+1,miny:maxy+1]
        cv2.imwrite("my_file.png",pic)

print(grains-1)
