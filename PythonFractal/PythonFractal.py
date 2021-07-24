
import cv2 as cv
import numpy as np
import time

width = 1200
height = 600
iterMax = 20

def onMouse(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
       

       print('x = %d, y = %d'%(x, y))

def coordToComplex(x,y,width,height):
    return complex((x/width)*4 - 2,(y/height)*2 - 1)
def drawFractal_Mandlebrot(image,width,height):
    for x in range(width):
        for y in range(height):
            image[y,x] = analyzePoint_Mandlebrot(coordToComplex(x,y,width,height))
    return image
def analyzePoint_Mandlebrot(c):
    z=c
    for i in range(iterMax):
        z = z*z + c
        if (abs(z) > 3):
            return [0,0,int((i/iterMax)*255)]
    return [0,0,0]

image = np.zeros((height,width,3),dtype = 'uint8')
start = time.time()
fractal = drawFractal_Mandlebrot(image,width,height)
end = time.time()
print(end-start)




cv.imshow("Mandlebrot",fractal)
cv.setMouseCallback("Mandlebrot", onMouse)
cv.waitKey(0)