#!/usr/bin/python

########################################################################################
#
# |B|I|G| |F|A|C|E| |R|O|B|O|T|I|C|S|
#
# HSV Colour selector for object detection using OpenCV
#
#
# Author : Peter Neal
#
# Date : 17 March 2015
# Last Update : 17 March 2015
#
########################################################################################

import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import imutils
from imutils.video import VideoStream
import datetime


def nothing(x):
    pass

print 'start OPENCV'

picamera = 1

vs = VideoStream(usePiCamera = picamera > 0 ).start()
'''
camera = PiCamera()
camera.resolution = (640,480)
camera.framerate = 16
rawCapture = PiRGBArray(camera, size = (640,480))
'''
print "WarmUp"
time.sleep(2)

time.sleep(0.1)
'''
camera.capture(rawCapture, format = "bgr")
image = rawCapture.array
'''
'''
capture = cv2.VideoCapture(0)

capture.set(3,640)
capture.set(4,480)
'''
cv2.namedWindow("camera", 0)
#print (Fore.GREEN + "Creating OpenCV windows")
cv2.resizeWindow("camera", 640,480) 
cv2.moveWindow("camera", 400,30)
#print (Fore.GREEN + "Moving OpenCV window")
cv2.waitKey(50)

#img = cv2.imread('t3.jpg',1)

# create trackbars for HSV Selection
print 'Create trackbars'
cv2.createTrackbar('HLow','camera',0,255,nothing)
cv2.createTrackbar('SLow','camera',0,255,nothing)
cv2.createTrackbar('VLow','camera',0,255,nothing)

cv2.createTrackbar('HHigh','camera',0,255,nothing)
cv2.createTrackbar('SHigh','camera',0,255,nothing)
cv2.createTrackbar('VHigh','camera',0,255,nothing)



while True:

    HLow = cv2.getTrackbarPos('HLow','camera')
    SLow = cv2.getTrackbarPos('SLow','camera')
    VLow = cv2.getTrackbarPos('VLow','camera')
    HHigh = cv2.getTrackbarPos('HHigh','camera')
    SHigh = cv2.getTrackbarPos('SHigh','camera')
    VHigh = cv2.getTrackbarPos('VHigh','camera')
    '''
    ret,img = capture.read() #get a bunch of frames to make sure current frame is the most recent
    ret,img = capture.read() 
    ret,img = capture.read()
    ret,img = capture.read()
    ret,img = capture.read() #5 seems to be enough
    '''
    #camera.capture_continuous(rawCapture, format = "bgr",use_video_port = True)
    #img = rawCapture.array
    #rawCapture.truncate(0)
    #img = cv2.imread('t3.jpg',1)

    frame = vs.read()
    #img = imutils.resize(frame, width =400)
    img = frame.copy()
    imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV) #convert img to HSV and store result in imgHSVyellow
    lower = np.array([HLow, SLow, VLow]) #np arrays for upper and lower thresholds
    upper = np.array([HHigh, SHigh, VHigh])

    imgthreshed = cv2.inRange(imgHSV, lower, upper) #threshold imgHSV
    #imgthreshed = cv2.blur(imgthreshed,(3,3))
    cv2.imshow("View", img)
    cv2.imshow("camera", imgthreshed)
    cv2.waitKey(10)

cv2.destroyAllWindows()








 
