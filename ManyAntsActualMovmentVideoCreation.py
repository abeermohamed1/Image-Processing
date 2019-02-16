# import the necessary packages
from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import math
import copy

out = cv2.VideoWriter('output/ActualManyAnts.avi', -1, 20.0, (1920,1080))
for m in range(0,132):
    out.write(cv2.imread("frames/actualMovment/frameoutput%d.jpg" % m))

out.release()
cv2.destroyAllWindows()