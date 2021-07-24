
import cv2 as cv
import numpy as np
import time
import cmath

width = 1200
height = 600
iterMax = 100
frames = 5


def onMouse(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
       print('x = %d, y = %d'%(x, y))

def coordToComplex(x,y,width,height):
    return complex((x/width)*4 - 2,(y/height)*2 - 1)
def drawFractal(width,height,iter,bail,analyzePoint):
    image = np.zeros((height,width,3),dtype = 'uint8')
    for x in range(width):
        for y in range(height):
            image[y,x] = analyzePoint(coordToComplex(x,y,width,height),iter,bail)
    return image
def analyzePoint_Mandlebrot(c,iter=20,bail=3):
    z=c
    for i in range(iter):
        z = z*z + c
        if (abs(z) > 3):
            return [int((i/iterMax)*255),int((i/iterMax)*255),int((i/iterMax)*255)]
    return [0,0,0]

def analyzePoint_custom1(c,iter=20,bail=3):
    z=c
    for i in range(iter):
        z = cmath.sqrt(c*z)*cmath.sqrt(c*z) + c
        if (abs(z) > 3):
            return [int((i/iterMax)*255),int((i/iterMax)*255),int((i/iterMax)*255)]
    return [0,0,0]

def createAndRunAnimation_itersPerFrame(width,height,fps,itersPerFrame,fractal):
    animation = np.zeros((frames,height,width,3),dtype = 'uint8')
    start = time.time()
    for f in range(1,frames+1):    
        animation[frames-f] = drawFractal(width,height,f*itersPerFrame,3,fractal)
    end = time.time()
    print("This animation took ", round(end-start,3), " seconds to render")
    runagain = True
    while runagain:
        for f in range(frames):
            if cv.waitKey(20) & 0xFF==ord('d'):
                runagain = False
                break
            time.sleep(fps**(-1))
            cv.imshow("Mandlebrot",animation[f])
        for f in range(frames-1,-1,-1):
            if cv.waitKey(20) & 0xFF==ord('d'):
                runagain = False
                break
            time.sleep(fps**(-1))
            cv.imshow("Mandlebrot",animation[f])


#image = np.zeros((height,width,3),dtype = 'uint8')
#start = time.time()
#fractal = drawFractal_Mandlebrot(image,width,height,20)
#createAndRunAnimation_itersPerFrame(width,height,5,10,analyzePoint_Mandlebrot)
createAndRunAnimation_itersPerFrame(width,height,5,20,analyzePoint_Mandlebrot)




#cv.imshow("Mandlebrot",fractal)
#cv.setMouseCallback("Mandlebrot", onMouse)
#cv.waitKey(0)