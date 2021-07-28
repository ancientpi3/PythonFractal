import cv2 as cv
import numpy as np
import time
import cmath
import math

WIDTH = 2080
HEIGHT = 1040
WidthHeightRatio = WIDTH/HEIGHT
ITERMAX = 50
iterPerFrame = 100
FRAMES = 60
SCALE = 1
XSHIFT = 0
YSHIFT = 0
FPS = 5
BAIL = 100

#Animation
#################################################################################################################################################
def createAnimation_itersPerFrame(fractal,itersPerFrame):
    animation = np.zeros((FRAMES,HEIGHT,WIDTH,3),dtype = 'uint8')
    start = time.time()
    for f in range(1,FRAMES+1):    
        animation[FRAMES-f] = drawFractal_analyzePoint(fractal,iter = f*itersPerFrame)
    end = time.time()
    print("This animation took ", round(end-start,3), " seconds to render")
    return animation
def createAnimation_Zoom(fractal,targetScale):
    animation = np.zeros((FRAMES,HEIGHT,WIDTH,3),dtype = 'uint8')
    start = time.time()
    for f in range(1,FRAMES+1):    
        animation[f-1] = drawFractal_analyzePoint(fractal, scale =  1- f*((1-targetScale)/FRAMES))
        print("Completed Frame ", f)
    end = time.time()
    print("This animation took ", round(end-start,3), " seconds to render")
    return animation

def RunAnimation(fps,animation):
    runagain = True
    while runagain:
        for f in range(FRAMES):
            if cv.waitKey(20) & 0xFF==ord('d'):
                runagain = False
                break
            time.sleep(FPS**(-1))
            cv.imshow("Mandlebrot",animation[f])
        for f in range(FRAMES-1,-1,-1):
            if cv.waitKey(20) & 0xFF==ord('d'):
                runagain = False
                break
            time.sleep(FPS**(-1))
            cv.imshow("Mandlebrot",animation[f])