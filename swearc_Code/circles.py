import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import imutils
from imutils.video import VideoStream
import datetime
import neatoCom as robot
import serial
import RPi.GPIO as GPIO
import sys

def RobotMove(distance, angle):
    #Implement code to move robot in desired way
    robot.iterativeTravel(angle,distance)
    return 1


def button_detect(image, ThresholdArray):
    #boundaries = [([0,125,125],[209,215,225])]
    #for (lower,upper) in boundaries:
    #    lower = np.array(lower,dtype="uint8")
    #    upper = np.array(upper,dtype="uint8")
    lower = np.array([ThresholdArray[0],ThresholdArray[1],ThresholdArray[2]]) #np arrays for upper and lower thresholds
    upper = np.array([ThresholdArray[3], ThresholdArray[4], ThresholdArray[5]])
    mask = cv2.inRange(image,lower,upper)
    #output = cv2.bitwise_and(image,image,mask=mask)
    #cv2.imshow("images",output)
    return mask

time.sleep(0.1)
'''
if DisplayImage is True:
    cv2.namedWindow("camera", 0)
    cv2.namedWindow("transform", 0)
    print  "Creating OpenCV windows"
    #cv2.waitKey(50)
    cv2.resizeWindow("camera", 640,480) 
    cv2.resizeWindow("transform", 300,300) 
    print  "Resizing OpenCV windows"
    #cv2.waitKey(50)
    cv2.moveWindow("camera", 400,30)
    cv2.moveWindow("transform", 1100,30)
    print  "Moving OpenCV window"
    cv2.waitKey(50)
'''
def find_button(imgHSV):
    Red_threshold = [0,132,124,209,232,223]
    Green_threshold = [32,63,106,84,210,167]
    boxcentrex= []
    boxcentrey= []
    area =[]
    '''
    img2 = button_detect(imgHSV, Red_threshold)
    print ' checking the button'
    #gray1 = cv2.cvtColor(img2,cv2.COLOR_HSV2GRAY)
    #cv2.imshow("gray",  gray1)
    _,contours, hierarchy = cv2.findContours(img2,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for x in range (len(contours)):
        contourarea = cv2.contourArea(contours[x]) #get area of contour
        if contourarea > 2500: #Discard contours with a small area as this may just be noise
            arclength = cv2.arcLength(contours[x], True)
            approxcontour = cv2.approxPolyDP(contours[x], 0.08 * arclength, True)
            #print len(approxcontour),' approxcontour'
            rect = cv2.minAreaRect(contours[x])
            #box = cv2.boxPoints(rect)
            #box = np.int0(box)
            print int(rect[0][0]),int(rect[0][1]),'centre'
            area.append(contourarea)
            boxcentrex.append(int(rect[0][0]))
            boxcentrey.append(int(rect[0][1]))
            cv2.drawContours(imgHSV,[approxcontour],0,(0,0,255),2)
            cv2.circle(imgHSV, (int(rect[0][0]), int(rect[0][1])), 5, (0,0,255),-1)
    '''
    img2 = button_detect(imgHSV, Green_threshold)
    print 'Checking Target'
    _,contours, hierarchy = cv2.findContours(img2,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for x in range (len(contours)):
        contourarea = cv2.contourArea(contours[x]) #get area of contour
        if contourarea > 2500: #Discard contours with a small area as this may just be noise
            arclength = cv2.arcLength(contours[x], True)
            approxcontour = cv2.approxPolyDP(contours[x], 0.08 * arclength, True)
            #print len(approxcontour),' approxcontour'
            rect = cv2.minAreaRect(contours[x])
            #box = cv2.boxPoints(rect)
            #box = np.int0(box)
            print int(rect[0][0]),int(rect[0][1]),'centre'
            area.append(contourarea)
            boxcentrex.append(int(rect[0][0]))
            boxcentrey.append(int(rect[0][1]))
            cv2.drawContours(imgHSV,[approxcontour],0,(0,0,255),2)
            cv2.circle(imgHSV, (int(rect[0][0]), int(rect[0][1])), 5, (0,0,255),-1)


    
    print 'boxcentrex',boxcentrex[0],boxcentrex[1],'boxcentrey',boxcentrey[0],boxcentrey[1]
    print 'area', area
    cv2.imshow("camera", imgHSV)
    return boxcentrex

def button_routine():
    img= vs.read()
    cv2.imshow('img',img)
    cv2.waitKey(1000)
    imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    xcord = find_button(imgHSV)
    return xcord


DisplayImage = 1
#unified Pi camera+ USB
picamera = 0

#vs = VideoStream(usePiCamera = picamera > 0 ).start()

'''

while True:

    #time.sleep(1)
    img= vs.read()
    imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    xcord = find_button(imgHSV)
    if (xcord[0]-xcord[1])>10:#ARM IS TO RIGHT
        RobotMove(0,-2)
        print 'arm right'
    elif (xcord[0]-xcord[1])<-10:
        RobotMove(0,2)
        print 'arm left'
    else:
        RobotMove(50,0)
        print 'move forward'
        print 'Task Fnished'
        GPIO.cleanup()
	robot.closeSerial()
        sys.exit('Button ROutine not defined')
	break
    
    cv2.waitKey(200)
'''
