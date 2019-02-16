
"""
Abeer Mohamed
"""
import os
import sys
import cv2 as cv2
import matplotlib.cm as cm
from scipy.ndimage import filters
import numpy as np
import pylab as plb
import matplotlib.pyplot as plt
import copy
import scipy.ndimage
import scipy.ndimage as nd
import matplotlib.pyplot as plt
_ALPHA = 300
_BETA = 2
_W_LINE = 80
_W_EDGE = 80
_NUM_NEIGHBORS = 9

# the candaidate 8 movment
neighbors = np.array([[i, j] for i in range(-1, 2) for j in range(-1, 2)])

# internal forces = summation from i to n alph * |Vi+1 - Vi|2 + BETA * |Vi+1 - 2* Vi + Vi-1 |2
def internalEnergy(snake):
    iEnergy=0
    snakeLength=len(snake)
    for index in range(snakeLength-1,-1,-1):
        nextPoint = (index+1)%snakeLength
        currentPoint = index % snakeLength
        previousePoint = (index - 1) % snakeLength
        iEnergy = iEnergy+ (_ALPHA *(np.linalg.norm(snake[nextPoint] - snake[currentPoint] )**2))\
                  + (_BETA * (np.linalg.norm(snake[nextPoint] - 2 * snake[currentPoint] + snake[previousePoint])**2))
    return iEnergy

# total energy for internal and external without constant
def totalEnergy(grediant, image, snake):
    iEnergy = internalEnergy(snake)
    eEnergy=externalEnergy(grediant, image, snake)
    tEnergy = iEnergy+eEnergy

    return tEnergy

#plot
def _display(image, changedPoint=None, snaxels=None):

    plb.clf()
    if snaxels is not None:
        for s in snaxels:
            if(changedPoint is not None and (s[0] == changedPoint[0] and s[1] == changedPoint[1])):
                plb.plot(s[0], s[1], 'r', markersize=10.0)
            else:
                plb.plot(s[0],s[1],'g.',markersize=10.0)

    plb.imshow(image, cmap=cm.Greys_r)
    plb.draw()
    
    return

# external forces summation of image grediant for all contour points
def externalEnergy(grediant,image,snak):
    sum = 0
    snaxels_Len = len(snak)
    for index in range(snaxels_Len - 1):
        point = snak[index]
        sum = +(image[point[1]][point[0]])
    pixel = 255 * sum

    eEnergy = _W_LINE*pixel -_W_EDGE*imageGradient(grediant, snak)

    return eEnergy

def interval_mapping(image, from_min, from_max, to_min, to_max):
    from_range = from_max - from_min
    to_range = to_max - to_min
    scaled = np.array((image - from_min) / float(from_range), dtype=float)
    return to_min + (scaled * to_range)

def basicImageGradiant(image):
    s_mask = 17
    sobelx = np.abs(cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=s_mask))
    sobelx = interval_mapping(sobelx, np.min(sobelx), np.max(sobelx), 0, 255)
    sobely = np.abs(cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=s_mask))
    sobely = interval_mapping(sobely, np.min(sobely), np.max(sobely), 0, 255)
    gradient = 0.5 * sobelx + 0.5 * sobely
    return gradient

def imageGradient(gradient, snak):
    sum = 0
    snaxels_Len= len(snak)
    for index in range(snaxels_Len-1):
        point = snak[index]
        sum = sum+((gradient[point[1]][point[0]]))
    return sum

def isPointInsideImage(image, point):

    return np.all(point < np.shape(image)) and np.all(point > 0)


def _pointsOnCircle(center, radius, num_points=12):
    points = np.zeros((num_points, 2), dtype=np.int32)
    for i in range(num_points):
        theta = float(i)/num_points * (2 * np.pi)
        x = center[0] + radius * np.cos(theta)
        y = center[1] + radius * np.sin(theta)
        p = [x, y]
        points[i] = p
        
    return points

def activeContour(image_file, center, radius):

    image = cv2.imread(image_file, 0)
    plb.ion()
    plb.figure(figsize=np.array(np.shape(image)) / 50.)

    snake = _pointsOnCircle(center, radius, 20)
    grediant = basicImageGradiant(image)
    plb.ioff()

    snakeColon =  copy.deepcopy(snake)

    for i in range(100):
        for index,point in enumerate(snake):
            min_energy2 = float("inf")
            for cindex,movement in enumerate(neighbors):
                next_node = (point +movement)
                if not isPointInsideImage(image, next_node):
                    continue
                if not isPointInsideImage(image, point):
                    continue

                snakeColon[index]=next_node

                totalEnergyNext = totalEnergy(grediant, image, snakeColon)

                if (totalEnergyNext < min_energy2):
                    min_energy2 = copy.deepcopy(totalEnergyNext)
                    indexOFlessEnergy = copy.deepcopy(cindex)
            snake[index] = (snake[index]+neighbors[indexOFlessEnergy])
        snakeColon = copy.deepcopy(snake)

    plb.ioff()
    _display(image,None, snake)
    plb.plot()
    plb.savefig(os.path.splitext(image_file)[0] + "-segmented.png")
    plb.show()

    return

def _test():

    activeContour("brainTumor.png", (98, 152), 30)
    return

if __name__ == '__main__':
    _test()