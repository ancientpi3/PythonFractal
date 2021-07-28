
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
ROOTS = [0+1j, 0-1j, -1] #changed to list of roots
EPSILON = .001
MAINIMAGE = None
def rootPolynomial(z):
    return z+(z-ROOTS[0])*(z-ROOTS[1])*(z-ROOTS[2])
#derivROOT1 = 1 + (ROOTS[0]-ROOTS[1])*(ROOTS[0]-ROOTS[2])
#derivROOT2 = 1 + (ROOTS[1]-ROOTS[0])*(ROOTS[1]-ROOTS[2])
#derivROOT3 = 1 + (ROOTS[2]-ROOTS[1])*(ROOTS[2]-ROOTS[0])

#derivROOTS = [derivROOT1,derivROOT2,derivROOT3]
def coordToComplex(x,y, scale=1, shiftx=0, shifty=0):
    return complex(scale*((x/WIDTH)*2*WidthHeightRatio - 2)+shiftx,scale*((y/HEIGHT)*WidthHeightRatio - 1)+shifty)
def complexToCoord(c,scale=1, shiftx=0, shifty=0):
   # print(c)
    x,y = int(((((c.real-shiftx)/scale)+2)/(2*WidthHeightRatio))*WIDTH), int(((((c.imag-shifty)/scale)+1)/(WidthHeightRatio))*HEIGHT)
    return (x,y)
    
def complexToColor(c,brightness=1):
    colorSens = 1
    b = int(255*(1/(1+math.exp(colorSens*-c.imag))*brightness))
    g = int(255*(1/(1+math.exp(colorSens*-c.imag))*brightness))
    r = int(255*(1/(1+math.exp(colorSens*-c.real))*brightness))
   #return [int((0.7*(1.0+math.sin(1.5*c.real))/2.0)*255),int((0.4*(1.0+math.sin(1.0*c.real))/2.0)*255),int((0.2*(1.0+math.sin(.5*c.real))/2.0)*255)]
    return [b,g,r]

def onMouse(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        print()
        #imagecopy = np.copy(MAINIMAGE)
        #drawIterationPath_Mandlebrot(coordToComplex(x,y),imagecopy)
def drawIterationPath_Mandlebrot(c,image):
    
    z=c
    z = z*z + c
    accumulator = 0
    cv.imshow("Fractal",cv.line(image,complexToCoord(c),complexToCoord(z),[255,0,0]))
    k=c
    for i in range(ITERMAX):
        accumulator = accumulator + z
        k = k*k+c
        z = z*z+c
        cv.line(image,complexToCoord(k),complexToCoord(z),[255,0,0])
    
    
    average = complexToCoord(accumulator/ITERMAX)
    image[average[1]][average[0]] = complexToColor(c)
    cv.imshow("Fractal",image)
    

#Other Fractal generations ########################################################################################################
def drawFractal_Average(averagePoint):
    image = np.zeros((HEIGHT,WIDTH,3),dtype = 'uint8')
    for x in range(WIDTH):
        for y in range(HEIGHT):
            #print(coordToComplex(x,y))
            averagePoint(coordToComplex(x,y),image)
    return image

def averagePoint_Mandlebrot(c,image,iter=ITERMAX,bail=BAIL):
    
    z=c
    z = z*z + c
    accumulator = 0
    
    
    for i in range(1,iter+1):
        accumulator = accumulator + z
        z = z*z+c
        if (abs(z)>bail):
            #print(c)
            bailPoint = complexToCoord(c)
            image[bailPoint[1]-1][bailPoint[0]-1] = complexToColor(c*(i/iter))
            return
    
    average = complexToCoord(accumulator/iter)
    image[average[1]-1][average[0]-1] = complexToColor(c)

def analyzePoint_MandleAverage(c,iter=ITERMAX,bail=BAIL):
    
    z=c
    z = z*z + c
    accumulator = 0
    
    
    for i in range(1,iter+1):
        accumulator = accumulator + z
        z = z*z+c
        if (abs(z)>bail):
            #print(c)
            bailPoint = complexToCoord(c)
            
            return complexToColor(c,(i/iter))
    
    return complexToColor(accumulator/iter)



#Fractal generation by point analysis
################################################################################################################################################





def drawFractal_analyzePoint(analyzePoint, scale=SCALE, iter = ITERMAX):
    image = np.zeros((HEIGHT,WIDTH,3),dtype = 'uint8')
    for x in range(WIDTH):
        for y in range(HEIGHT):
            image[y,x] = analyzePoint(coordToComplex(x,y,scale,XSHIFT,YSHIFT),iter=iter)
    return image

def analyzePoint_colorPlane(c,iter):
    return complexToColor(c)

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
def analyzePoint_poly(c,iter=10,epsilon=EPSILON,bail = 13):
    z = rootPolynomial(c) # z is one iteration in front of c
    
    for i in range(1,iter):
        c = rootPolynomial(c)
        z = rootPolynomial(z)
     
        
    if (abs(z)>bail):
        return [0,0,0]
        #part of the algorithm that sees if the point is iterating to the stable point
        #for i in range(len(ROOTS)):
        #    if (abs(z-ROOTS[i]) < epsilon):
        #        trueIterNumber = cmath.log((c-ROOTS[i])/(derivROOTS[i]**i),cmath.e)
        #        return complexToColor(trueIterNumber)
        #part of the algorithm that sees if the point bails
        #if (abs(z) > bail):
        #    #return ([255,255,255])
        #    return [0,0,0]
    return ([100,100,100])


def analyzePoint_custom2(c, iter = 100,bail = BAIL):
    z=c
    for i in range(iter):
        z = cmath.sqrt(z) * cmath.sqrt(c)

        if (abs(z)>bail):
            return [100,0,0]
    return [0,0,0]





#
#
#
#
#

#image = np.zeros((height,width,3),dtype = 'uint8')
#start = time.time()
#fractal = drawFractal_analyzePoint(width,height,100,3,analyzePoint_custom1)
#isWritten = cv.imwrite('C:/Users/Ethan/source/repos/PythonFractal/PythonFractal/Saved Fractals/custom1.png', fractal)
#RunAnimation(createAnimation_itersPerFrame(analyzePoint_Mandlebrot,iterPerFrame))
#RunAnimation(FPS,createAnimation_Zoom(analyzePoint_Mandlebrot,.02))
#createAndRunAnimation_itersPerFrame(width,height,5,20,analyzePoint_custom1)





#fourcc = cv.VideoWriter_fourcc(*'MP42')
#video = cv.VideoWriter('C:/Users/Ethan/source/repos/PythonFractal/PythonFractal/Saved Fractals/MandleBrotZoom.mp4', fourcc, float(FPS), (WIDTH, HEIGHT))

#for frame in createAnimation_Zoom(analyzePoint_Mandlebrot,.002):
#    video.write(frame)
#video.release()
#writer = cv.VideoWriter('C:/Users/Ethan/source/repos/PythonFractal/PythonFractal/Saved Fractals/test1.mp4', cv.VideoWriter_fourcc(*'mp4v'), FPS, (size[1], size[0]))
#writer.write(createAnimation_Zoom(analyzePoint_Mandlebrot,.02))


#MAINIMAGE = drawFractal_analyzePoint(analyzePoint_Mandlebrot_Average)

MAINIMAGE = drawFractal_analyzePoint(analyzePoint_colorPlane)
isWritten = cv.imwrite('C:/Users/Ethan/source/repos/PythonFractal/PythonFractal/Saved Fractals/fractal.png', MAINIMAGE)
cv.imshow("Fractal",MAINIMAGE)
cv.setMouseCallback("Fractal", onMouse)
cv.waitKey(0)



