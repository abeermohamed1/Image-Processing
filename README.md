# Image-Processing and Computer Vision
Image Processing and Computer Vision tasks using OpenCV Python: motion tracking, face detection, tumor segmentation.

* **1. [Face Detection](https://github.com/abeermohamed1/Image-Processing/blob/master/faceDetection.py):**
**(faceDetection.py)**
Face detection python code, which detect the faces for all images located in the folder path: "./people/" the tested images is from yelp dataset.  The output of the program is detecting all faces in the images then save them in the output folder "./peopleOut2/". The applied algorithm is haarcascades using OpenCV python library.

* **2. [Brain Tumor segmentation](https://github.com/abeermohamed1/Image-Processing/blob/master/activeContour.py):**
**(activeContour.py, brainTumor.png, brainTumor-segmented.png)**
Segmentation Python code for brain tumor using Active Contour model.
The program output is new image after segmenting the brain tumor using OpenCV python library.

* **3. [Ant Motion Tracking](https://github.com/abeermohamed1/Image-Processing/blob/master/ManyAntsActualMovment.py) :**
**(ManyAntsActualMovment.py, ManyAntsActualMovmentVideoCreation.py, ManyAnts.mov, ActualManyAnts.avi)**
Ant motion tracking python program using Python OpenCV library. The ManyAntsActualMovement.py file is containing the tracking program which alter every frame in the video by the ants tracking. Then the ManyAntsVideoCreation.py file append all frames to perform a new video with ant tracking.
The ManyAnts.mov video is the original video before applying the motion tracking,the ActualManyAnts.avi is the output video after applying the motion tracking.

* **4. [Expecting Ant Motion Tracking](https://github.com/abeermohamed1/Image-Processing/blob/master/ManyAntsExpected.py) :**
**(ManyAntsExpected.py, ManyAntsVideoCreation.py, ManyAnts.mov, ExpectedManyAnts3.avi)**
Ant expecting motion tracking python program using Python OpenCV library. The ManyAntsExpected.py file is containing the tracking program which alter every frame in the video by the ants "expected" track. Then the ManyAntsVideoCreation.py file append all frames to perform a new video with ant expected tracking.
The ManyAnts.mov video is the original video before applying the motion tracking,the ExpectedManyAnts3.avi is the output video after applying the motion expected tracking.

Hope this will be helpfull.
