from math import *
import random

chars = ". , - + * $ & # @ ~ ~ ".split()
(rows,cols) = (40,80)
points = 8  
xfact = 1.0/rows
yfact = 1.0/cols
xs = []
ys = []

#generate a few random points v1...vn
for i in range(0,points):
    (xrand,yrand) = (random.random(),random.random())
    print "%f %f"%(xrand,yrand)
    for xoff in range(-1,2):
        for yoff in range(-1,2):
            xs.append(xrand+xoff)            
            ys.append(yrand+yoff)

#function to find the closest of the vi
def closest(x,y,xs,ys):
    (best,good) = (99.0,99.0)
    for i in range(0,len(xs)):
        dist = sqrt((x-xs[i])**2.0+(y-ys[i])**2.0)
        if (dist < best):
            (best,good) = (dist,best)
        elif dist < good:
            good = dist
    return (best,good)

screen = []
for i in range(0,rows):
    screen.append(" ")
 
#generate screen 
for i in range(0,rows):
    x = i*xfact;
    for j in range(0,cols):
        y = j*yfact;
        (best,good) = closest(x,y,xs,ys)
        screen[i] = screen[i] + chars[int(10*best/good)]

for i in range(0,rows):
    print screen[i]
