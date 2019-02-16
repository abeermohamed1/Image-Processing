# import the necessary packages
from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import math
import copy

# to check if two contours very close then will compine them
def find_if_close(cnt1,cnt2):
    row1,row2 = cnt1.shape[0],cnt2.shape[0]
    for i in xrange(row1):
        for j in xrange(row2):
            dist = np.linalg.norm(cnt1[i]-cnt2[j])
            if abs(dist) < 50 :
                return True
            elif i==row1-1 and j==row2-1:
                return False

def pointAverage(point1,point2):
    x1 = point1[0]
    y1 = point1[1]

    x2 = point2[0]
    y2 = point2[1]

    x3 = (x2 + x1) / 2
    y3 = (y2 + y1) / 2
    return (x3, y3)

def calculateNextPoint(point1,point2):
    x1 = point1[0]
    y1 = point1[1]

    x2 = point2[0]
    y2 = point2[1]

    x3 = x2 + (x2 - x1)
    y3 = y2 + (y2 - y1)
    return (x3, y3)

# threashold for bloack color
greenLower = (19, 15, 34)
greenUpper = (30, 22, 46)
pts = deque(maxlen=32)
counter = 0

camera = cv2.VideoCapture("Sample_Tracking_Release/Many_Ants/ManyAnts.mov")
histroy = []
histroy.append(deque())
nextPoint = []
nextPoint.append(deque())
frameIndex = 0
while True:
    # grab the current frame
    (grabbed, frame) = camera.read()
    if not grabbed:
        break

    hsv = cv2.cvtColor(frame, cv2.CAP_MODE_RGB)
    mask = cv2.inRange(hsv, greenLower, greenUpper)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)[-2]

    center = None
    # only proceed if at least one contour was found
    if len(cnts) > 0:

        LENGTH = len(cnts)
        status = np.zeros((LENGTH, 1))
        for i, cnt1 in enumerate(cnts):
            x = i
            if i != LENGTH - 1:
                for j, cnt2 in enumerate(cnts[i + 1:]):
                    x = x + 1
                    dist = find_if_close(cnt1, cnt2)
                    if dist == True:
                        val = min(status[i], status[x])
                        status[x] = status[i] = val
                    else:
                        if status[x] == status[i]:
                            status[x] = i + 1

        unified = []
        maximum = int(status.max()) + 1
        for i in xrange(maximum):
            pos = np.where(status == i)[0]
            if pos.size != 0:
                c = np.vstack(cnts[i] for i in pos)
                hull = cv2.convexHull(c)
                unified.append(hull)

            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            drwaCirlce= "no"
            if(len(cnts) >2):
                if(M["m00"] >0):
                    center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                    drwaCirlce = "yes"
                else:
                    center = (cnts[0][:, 0][0, 0], cnts[0][:, 0][0, 1])
            else:
                center =(cnts[0][:,0][0,0],cnts[0][:,0][0,1])

            if(drwaCirlce is "yes"):

                cricle1 = cv2.circle(frame, (int(x), int(y)), int(50),
                           (0, 255, 255), 2)

                pts.appendleft((int(x), int(y)))
                if histroy is not None:
                    histroy[frameIndex].appendleft(copy.deepcopy((int(x), int(y))))

    if frameIndex > 0:
        for j in range(0, frameIndex):

        #for j in range(frameIndex, frameIndex-2, -1):
            if len(histroy[j]) < len(histroy[j - 1]):
                min1 = len(histroy[j])
            else:
                min1 = len(histroy[j - 1])
            for i in np.arange(0, min1):

                if j >0 and len(histroy[j])>0 :
                    dist = math.hypot(histroy[j][i][0] - histroy[j-1][i][0], histroy[j][i][1] - histroy[j-1][i][1])

                    if j >=3:

                        if histroy[j - 2] is not None and len(histroy[j - 2])-1>= i :
                            comingPoint = calculateNextPoint(histroy[j - 2][i],
                                                             histroy[j - 1][i])

                            avgPoint = pointAverage(comingPoint, histroy[j][i])
                            #print "p1, ", histroy[j - 2][i], "p2,", histroy[j - 1][i], "p3'", comingPoint, "p3", histroy[j][i], "avgPoint",avgPoint

                            dist1 = math.hypot(comingPoint[0] - histroy[j - 1][i][0],
                                               comingPoint[1] - histroy[j - 1][i][1])
                            """

                            dist1 = math.hypot(avgPoint[0] - histroy[j - 1][i][0],
                                               avgPoint[1] - histroy[j - 1][i][1])
                            """
                            if dist1 < 35:

                                cv2.line(frame, histroy[j-1][i], comingPoint, (87, 255, 46), 5)

                                #cv2.line(frame, histroy[j - 1][i], avgPoint, (87, 255, 46), 5)
                                #histroy[j][i] = avgPoint

                    else:
                        if dist < 35:
                            cv2.line(frame, histroy[j-1][i], histroy[j][i], (0, 0, 255), 5)

    if len(histroy[frameIndex]) > 0 :
        histroy.append(deque())
        nextPoint.append(deque())
        frameIndex += 1

    cv2.namedWindow('Frame', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Frame', 500, 500)
    cv2.imshow("Frame", frame)
    name = "frames/manyAnts/frameoutput%d.jpg" % counter
    cv2.imwrite(name, frame)
    key = cv2.waitKey(1) & 0xFF
    counter += 1

    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break


camera.release()
cv2.destroyAllWindows()
