
import cv2 as cv
import numpy as np
import time

width = 1200
height = 600
iterMax = 100
frames = 15

def onMouse(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
       print('x = %d, y = %d'%(x, y))

def coordToComplex(x,y,width,height):
    return complex((x/width)*4 - 2,(y/height)*2 - 1)
def drawFractal_Mandlebrot(width,height,iter):
    image = np.zeros((height,width,3),dtype = 'uint8')
    for x in range(width):
        for y in range(height):
            image[y,x] = analyzePoint_Mandlebrot(coordToComplex(x,y,width,height),iter)
    return image
def analyzePoint_Mandlebrot(c,iter):
    z=c
    for i in range(iter):
        z = z*z + c
        if (abs(z) > 3):
            return [0,0,int((i/iterMax)*255)]
    return [0,0,0]

def createAndRunAnimation_fractal(width,height,fps,fractal):
    animation = np.zeros((frames,height,width,3),dtype = 'uint8')
    start = time.time()
    for f in range(frames):    
        animation[f] = fractal(width,height,f*4)
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


#image = np.zeros((height,width,3),dtype = 'uint8')
#start = time.time()
#fractal = drawFractal_Mandlebrot(image,width,height,20)
createAndRunAnimation_fractal(width,height,5,drawFractal_Mandlebrot)





#cv.imshow("Mandlebrot",fractal)
#cv.setMouseCallback("Mandlebrot", onMouse)
#cv.waitKey(0)