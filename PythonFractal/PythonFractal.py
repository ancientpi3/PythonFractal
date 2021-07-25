
import cv2 as cv
import numpy as np
import time
import cmath

WIDTH = 1200
HEIGHT = 600
ITERMAX = 100
iterPerFrame = 100
FRAMES = 3
SCALE = 1
XSHIFT = 0
YSHIFT = 0
FPS = 5
BAIL = 3



def onMouse(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
       print('x = %d, y = %d'%(x, y))

#Fractal generation
################################################################################################################################################

def coordToComplex(x,y, scale, shiftx=0, shifty=0):
    return complex(scale*((x/WIDTH)*4 - 2)+shiftx,scale*((y/HEIGHT)*2 - 1)+shifty)
def drawFractal(analyzePoint, scale=SCALE, iter = ITERMAX):
    image = np.zeros((HEIGHT,WIDTH,3),dtype = 'uint8')
    for x in range(WIDTH):
        for y in range(HEIGHT):
            image[y,x] = analyzePoint(coordToComplex(x,y,scale,XSHIFT,YSHIFT),iter=iter)
    return image
def analyzePoint_Mandlebrot(c,iter=20):
    z=c
    for i in range(iter):
        z = z*z + c
        if (abs(z) > 3):
            return [int((i/iter)*255),int((i/iter)*255),int((i/iter)*255)]
    return [0,0,0]

def analyzePoint_custom1(c,iter=20):
    z=c
    for i in range(iter):
        z = complex(1,2)*z + z*z +c
        if (abs(z) > 3):
            return [int((i/iter)*255),int((i/iter)*255),int((i/iter)*255)]
    return [0,0,0]
#Animation
#################################################################################################################################################
def createAnimation_itersPerFrame(fractal,itersPerFrame):
    animation = np.zeros((FRAMES,HEIGHT,WIDTH,3),dtype = 'uint8')
    start = time.time()
    for f in range(1,FRAMES+1):    
        animation[FRAMES-f] = drawFractal(fractal,iter = f*itersPerFrame)
    end = time.time()
    print("This animation took ", round(end-start,3), " seconds to render")
    return animation
def createAnimation_Zoom(fractal,targetScale):
    animation = np.zeros((FRAMES,HEIGHT,WIDTH,3),dtype = 'uint8')
    start = time.time()
    for f in range(1,FRAMES+1):    
        animation[f-1] = drawFractal(fractal, scale =  1- f*((1-targetScale)/FRAMES))
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


#
#
#
#
#

#image = np.zeros((height,width,3),dtype = 'uint8')
#start = time.time()
#fractal = drawFractal(width,height,100,3,analyzePoint_custom1)
#isWritten = cv.imwrite('C:/Users/Ethan/source/repos/PythonFractal/PythonFractal/Saved Fractals/custom1.png', fractal)
#RunAnimation(createAnimation_itersPerFrame(analyzePoint_Mandlebrot,iterPerFrame))
RunAnimation(FPS,createAnimation_Zoom(analyzePoint_Mandlebrot,.5))
#createAndRunAnimation_itersPerFrame(width,height,5,20,analyzePoint_custom1)
#writer = cv.VideoWriter('C:/Users/Ethan/source/repos/PythonFractal/PythonFractal/Saved Fractals/test1.mp4', fourcc, FPS, (WDITH, HEIGHT))
#writer.release() 



#cv.imshow("Mandlebrot",fractal)
#cv.setMouseCallback("Mandlebrot", onMouse)
#cv.waitKey(0)