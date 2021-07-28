
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
BAIL = 3

#ROOTS = [0+1j, 0-1j, -1] #changed to list of roots
#EPSILON = .001
MAINIMAGE = None
def onMouse(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        print()
        imagecopy = np.copy(MAINIMAGE)
        drawIterationPath(coordToComplex(x,y),FUNCTION,imagecopy)
def drawIterationPath(c,function,image):
    z=c
    z = function(z,c)
    accumulator = 0
    cv.imshow("Fractal",cv.line(image,complexToCoord(c),complexToCoord(z),[255,0,0]))
    k=c
    for i in range(ITERMAX):
        accumulator = accumulator + z
        k = function(k,c)
        z = function(z,c)
        cv.line(image,complexToCoord(k),complexToCoord(z),[255,0,0])
        
    
    average = complexToCoord(accumulator/ITERMAX)
    image[average[1]][average[0]] = complexToColor(c)
    cv.imshow("Fractal",image)



def coordToComplex(x,y, scale=1, shiftx=0, shifty=0):
    return complex(scale*((x/WIDTH)*2*WidthHeightRatio - 2)+shiftx,scale*((y/HEIGHT)*WidthHeightRatio - 1)+shifty)




def complexToCoord(c,scale=1, shiftx=0, shifty=0):
   # print(c)
    x,y = int(((((c.real-shiftx)/scale)+2)/(2*WidthHeightRatio))*WIDTH), int(((((c.imag-shifty)/scale)+1)/(WidthHeightRatio))*HEIGHT)
    return (x,y)


def drawFractal(function,iter=ITERMAX,bail=BAIL):
    image = np.zeros((HEIGHT,WIDTH,3),dtype = 'uint8')
    for x in range(WIDTH):
        for y in range(HEIGHT):
            c = coordToComplex(x,y)
            z=c
            for i in range(iter):
                z = function(z,c)
                if (abs(z)>bail):
                    image[y][x] = [0,0,0]
                    break
            image[y][x]=[255,255,255]
    return image

def mandlebrot(z,c):
    return z*z+c




FUNCTION = mandlebrot
MAINIMAGE = drawFractal(FUNCTION)
cv.imshow("Fractal",MAINIMAGE)
cv.setMouseCallback("Fractal", onMouse)
cv.waitKey(0)



