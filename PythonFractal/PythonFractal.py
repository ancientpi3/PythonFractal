
import cv2 as cv
import numpy as np
import time
import cmath
import math

WIDTH = 1400
HEIGHT = 700
WidthHeightRatio = WIDTH/HEIGHT
ITERMAX = 50
SCALE = 1
XSHIFT = 0
YSHIFT = 0
BAIL = 1000

#ROOTS = [0+1j, 0-1j, -1] #changed to list of roots
#EPSILON = .001
MAINIMAGE = None
def onMouse(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        print()
    
def coordToComplex(x,y, scale=1, shiftx=0, shifty=0):
    #dddd
    return complex(scale*((x/WIDTH)*2*WidthHeightRatio - 2)+shiftx,scale*((y/HEIGHT)*WidthHeightRatio - 1)+shifty)
def complexToCoord(c,scale=1, shiftx=0, shifty=0):
   # print(c)
    x,y = int(((((c.real-shiftx)/scale)+2)/(2*WidthHeightRatio))*WIDTH), int(((((c.imag-shifty)/scale)+1)/(WidthHeightRatio))*HEIGHT)
    return (x,y)


def drawFractal(function,iter=ITERMAX,bail=BAIL):
    image = np.zeros((HEIGHT,WIDTH,3),dtype = 'uint8')
    for x in range(WIDTH):
        for y in range(HEIGHT):
            image[y][x]=function(coordToComplex(x,y))
    return image

def mandlebrot(c,iter=ITERMAX,bail=BAIL):
    z=c
    acc = 0
    for i in range(iter):
        z = z*z+c
        acc = acc+z
        if (abs(z.imag) >bail):
            color = int((i/iter)*255)
            return [color,color,color]
        if (abs(z.real) >bail):
            color = int((i/iter)*255)
            return [color,color,color]

            
    averageC = acc/iter
    color = int(255 * (abs(averageC)))
    return [color,color,color]
        
                    





MAINIMAGE = drawFractal(mandlebrot)
cv.imshow("Fractal",MAINIMAGE)
cv.setMouseCallback("Fractal", onMouse)
cv.waitKey(0)



