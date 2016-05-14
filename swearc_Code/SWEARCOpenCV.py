   
# |B|I|G| |F|A|C|E| |R|O|B|O|T|I|C|S|

#import cv
import time
import cv2
import numpy as np
import sys
import math
from pyimagesearch.transform import four_point_transform

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
import zbar
from PIL import Image
import json
from sys import argv


DisplayImage = True


print "Starting OpenCV"
'''
capture = cv2.VideoCapture(0)

capture.set(3,640) #1024 640 1280 800 384
capture.set(4,480) #600 480 960 600 288
'''
#unified Pi camera+ USB
picamera = 0

vs = VideoStream(usePiCamera = picamera > 0 ).start()


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

##################################################################################################
#
# Set up detectors for symbols
#
##################################################################################################
'''
detector = cv2.SURF(1000)
HomeSymbol = cv2.imread("homesymbol.png")
HomeSymbolKeypoints, HomeSymbolDescriptors = detector.detectAndCompute(HomeSymbol , None)
FoodSymbol = cv2.imread("foodsymbol.png")
FoodSymbolKeypoints, FoodSymbolDescriptors = detector.detectAndCompute(FoodSymbol , None)
FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks = 50)
matcher = cv2. FlannBasedMatcher(index_params, search_params)

##################################################################################################
#
# Display image - Capture a frame and display it on the screen
#
##################################################################################################
def DisplayFrame():

    ret,img = capture.read()
    ret,img = capture.read()
    ret,img = capture.read()
    ret,img = capture.read()
    ret,img = capture.read() #get a bunch of frames to make sure current frame is the most recent

    cv2.imshow("camera", img)
    cv2.waitKey(10)
'''
##################################################################################################
#
# Reform Contours - Takes an approximated array of 4 pairs of coordinates and puts them in the order
# TOP-LEFT, TOP-RIGHT, BOTTOM-RIGHT, BOTTOM-LEFT
#
##################################################################################################
def ReformContours(contours):
        contours = contours.reshape((4,2))
        contoursnew = np.zeros((4,2),dtype = np.float32)
 
        add = contours.sum(1)
        contoursnew[0] = contours[np.argmin(add)]
        contoursnew[2] = contours[np.argmax(add)]
         
        diff = np.diff(contours,axis = 1)
        contoursnew[1] = contours[np.argmin(diff)]
        contoursnew[3] = contours[np.argmax(diff)]
  
        return contoursnew

##################################################################################################
#
# FindSymbol
#
##################################################################################################

def FindSymbol(ThresholdArray):

    TargetData = -1
    SymbolFound = -1
    vmfound = -1
    time.sleep(0.1)#let image settle
    frame = vs.read()
    img = frame.copy()
    imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV) #convert img to HSV and store result in imgHSVyellow
    lower = np.array([ThresholdArray[0],ThresholdArray[1],ThresholdArray[2]]) #np arrays for upper and lower thresholds
    upper = np.array([ThresholdArray[3], ThresholdArray[4], ThresholdArray[5]])

    imgthreshed = cv2.inRange(imgHSV, lower, upper) #threshold imgHSV

    _,contours, hierarchy = cv2.findContours(imgthreshed,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)  
    
    for x in range (len(contours)):
        contourarea = cv2.contourArea(contours[x]) #get area of contour
        if contourarea > 400: #Discard contours with a small area as this may just be noise
            arclength = cv2.arcLength(contours[x], True)
            approxcontour = cv2.approxPolyDP(contours[x], 0.08 * arclength, True) #Approximate contour to find square objects
            if len(approxcontour) == 4: #if approximated contour has 4 corner points
                if hierarchy[0][x][2] != -1: #if contour has a child contour, which is image in centre of border
                    #find centre point of target
                    rect = cv2.minAreaRect(contours[x])
                    box = cv2.boxPoints(rect)
                    box = np.int0(box)
                    boxcentrex = int(rect[0][0])
                    boxcentrey = int(rect[0][1])
                    #correct perspective of found target and output to image named warp      
                    reformedcontour = ReformContours(approxcontour) #make sure coordinates are in the correct order
                    warp = four_point_transform(img.copy(), approxcontour.reshape(4, 2))
                    cv2.imshow("transform", warp)
                    cv2.waitKey(10)
                    new_vm = warp.copy()
                    gray1 = cv2.cvtColor(new_vm, cv2.COLOR_BGR2GRAY)
                    vmfound = 1
                    #Try and match image to known targets
                    '''
                    circles = cv2.HoughCircles(gray1.copy(), cv2.HOUGH_GRADIENT, 1.2, 100,param1=50,param2=90,minRadius=1,maxRadius=200)
                    # ensure at least some circles were found
                    if circles is not None:
                        # convert the (x, y) coordinates and radius of the circles to integers
                        circles = np.round(circles[0, :]).astype("int")
                        # loop over the (x, y) coordinates and radius of the circles
                        for (x, y, r) in circles:
                            # draw the circle in the output image, then draw a rectangle
                            # corresponding to the center of the circle
                            cv2.circle(new_vm, (x, y), r, (0, 255, 0), 4)
                            cv2.rectangle(new_vm, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
                        # show the output image
                        cv2.imshow("output",  new_vm)
                        vmfound = 1
                        #cv2.waitKey(0)
                    else:
                        print 'Circles are Doomed'
                        #return -1
                    '''

                    #Find lengths of the 4 sides of the target
                    leftedge = reformedcontour[3][1] - reformedcontour[0][1]
                    rightedge = reformedcontour[2][1] - reformedcontour[1][1]
                    topedge = reformedcontour[1][0] - reformedcontour[0][0]
                    bottomedge = reformedcontour[2][0] - reformedcontour[3][0]
                    print 'Side Leghts',leftedge,rightedge,topedge,bottomedge
                    #print 'Reform Contour', reformedcontour
                    #Find approximate distance to target
                    if leftedge > rightedge:
                        LongestSide = leftedge
                    else:
                        LongestSide = rightedge
                    if topedge > LongestSide:
                        LongestSide = topedge
                    if bottomedge > LongestSide:
                        LongestSide = bottomedge
                    Distance = (640.00*30)/LongestSide #focal length x Actual Border width / size of Border in pixels
                    print "Distance= " + str(Distance)

                    #Find which way symbol is facing and width of target to gauge angle
                    EdgeDifference = leftedge - rightedge
                    if EdgeDifference > 0:
                        print "Symbol is to the robots right"
                        SymbolLocation = "RIGHT"
                    elif EdgeDifference == 0:
                        print "Symbol is dead ahead"
                        SymbolLocation = "AHEAD"
                    else:
                        print "Symbol is to the robots left"
                        SymbolLocation = "LEFT"

                    width = (topedge + bottomedge) / 2
                    height = (leftedge + rightedge) / 2
                    whratio = width / height
                    #print  "Edge Difference = "  str(EdgeDifference)
                    #time.sleep(1)

                    #draw box around target and a circle to mark the centre point
                    cv2.drawContours(img,[approxcontour],0,(0,0,255),2)
                    cv2.circle(img, (boxcentrex, boxcentrey), 5, (0,0,255),-1) #draw a circle at centre point of object
                    
                    TextForScreen = "Approx. Distance: " + "%.2f" % Distance + "cm"
                    cv2.putText(img,TextForScreen, (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0,255,0),1)

                    if vmfound != -1: #If a symbol has been found
                        #write symbol type to screen
                        TextForScreen = "Found: Vending Machine" 
                        cv2.putText(img,TextForScreen, (10,60), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0,255,0),1)
                        #Only return data is a target has been identified
                        TargetData = [boxcentrex, boxcentrey, Distance, vmfound, SymbolLocation, EdgeDifference]
                        break
                        
          
    if DisplayImage is True:
        cv2.imshow("camera", img)
        cv2.waitKey(10)

    return TargetData




def Find_red_circles(ThresholdArray):

    TargetData = -1
    SymbolFound = -1
    vmfound = -1
    time.sleep(0.1)#let image settle
    frame = vs.read()
    img = frame.copy()
    imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV) #convert img to HSV and store result in imgHSVyellow
    lower = np.array([ThresholdArray[0],ThresholdArray[1],ThresholdArray[2]]) #np arrays for upper and lower thresholds
    upper = np.array([ThresholdArray[3], ThresholdArray[4], ThresholdArray[5]])
    imgthreshed = cv2.inRange(imgHSV, lower, upper) #threshold imgHSV
    cv2.imshow("output",  imgthreshed)
    cv2.waitKey(1000)
    print 'For loop'
    # Contours and stuff
    _,contours, hierarchy = cv2.findContours(imgthreshed,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)  
    for x in range (len(contours)):
        contourarea = cv2.contourArea(contours[x]) #get area of contour
        if contourarea > 400: #Discard contours with a small area as this may just be noise
            arclength = cv2.arcLength(contours[x], True)
            approxcontour = cv2.approxPolyDP(contours[x], 0.01 * arclength, True) #Approximate contour to find square objects
            print 'dimensions', len(approxcontour)
            if len(approxcontour) >= 8: #if approximated contour has 4 corner points
                vmfound = 1
                rect = cv2.minAreaRect(contours[x])
                print rect
                boxcentrex = int(rect[0][0])
                boxcentrey = int(rect[0][1])

                #############
                #For finding the distance of rectangle
                #############
                
                approxcontour = cv2.approxPolyDP(contours[x], 0.08 * arclength, True) #Approximate contour to find square objects
                print 'dimensions', len(approxcontour)
                if len(approxcontour) == 4: #if approximated contour has 4 corner points
                    rect = cv2.minAreaRect(contours[x])
                    reformedcontour = ReformContours(approxcontour) #make sure coordinates are in the correct order

                    leftedge = reformedcontour[3][1] - reformedcontour[0][1]
                    rightedge = reformedcontour[2][1] - reformedcontour[1][1]
                    topedge = reformedcontour[1][0] - reformedcontour[0][0]
                    bottomedge = reformedcontour[2][0] - reformedcontour[3][0]
                    print 'Side Leghts',leftedge,rightedge,topedge,bottomedge
                    #print 'Reform Contour', reformedcontour
                    #Find approximate distance to target
                    if leftedge > rightedge:
                        LongestSide = leftedge
                    else:
                        LongestSide = rightedge
                    if topedge > LongestSide:
                        LongestSide = topedge
                    if bottomedge > LongestSide:
                        LongestSide = bottomedge
                    Distance = (640.00*5)/LongestSide #focal length x Actual Border width / size of Border in pixels
                    print "Distance= " + str(Distance)
                    #Find which way symbol is facing and width of target to gauge angle
                    EdgeDifference = leftedge - rightedge
                    if EdgeDifference > 0:
                        print "Symbol is to the robots right"
                        SymbolLocation = "RIGHT"
                    elif EdgeDifference == 0:
                        print "Symbol is dead ahead"
                        SymbolLocation = "AHEAD"
                    else:
                        print "Symbol is to the robots left"
                        SymbolLocation = "LEFT"

                    width = (topedge + bottomedge) / 2
                    height = (leftedge + rightedge) / 2
                    whratio = width / height
                    cv2.drawContours(img,[approxcontour],0,(0,0,255),2)
                    cv2.circle(img, (boxcentrex, boxcentrey), 5, (0,0,255),-1) #draw a circle at centre point of object        
                    TextForScreen = "Approx. Distance: " + "%.2f" % Distance + "cm"
                    cv2.putText(img,TextForScreen, (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0,255,0),1)
                    if vmfound != -1: #If a symbol has been found
                        #write symbol type to screen
                        TextForScreen = "Found: Vending Machine" 
                        cv2.putText(img,TextForScreen, (10,60), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0,255,0),1)
                        #Only return data is a target has been identified
                        TargetData = [boxcentrex, boxcentrey, Distance, vmfound, SymbolLocation, EdgeDifference]
                        print TargetData
                        break
                    
    cv2.imshow("output",  imgthreshed)
    return TargetData
    #Circles 
    '''
    imgHSV = cv2.bitwise_and(img,img,mask = imgthreshed)
    gray = cv2.cvtColor(imgHSV,cv2.COLOR_BGR2GRAY)
    
    circles = cv2.HoughCircles(gray.copy(), cv2.HOUGH_GRADIENT, 1.2, 100,param1=50,param2=90,minRadius=1,maxRadius=10000)
    cv2.imshow("output",  gray)
    cv2.waitKey(1000)
    # ensure at least some circles were found
    if circles is not None:
        # convert the (x, y) coordinates and radius of the circles to integers
        circles = np.round(circles[0, :]).astype("int")
        # loop over the (x, y) coordinates and radius of the circles
        for (x, y, r) in circles:
            # draw the circle in the output image, then draw a rectangle
            # corresponding to the center of the circle
            cv2.circle(new_vm, (x, y), r, (0, 255, 0), 4)
            cv2.rectangle(new_vm, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
            # show the output image
        cv2.imshow("output",  new_vm)
        vmfound = 1
        #cv2.waitKey(0)
    else:
        print 'Circles are Doomed'
    return 1
    '''             

#########################################################################
##
## Functions for Circles
##
#########################################################################    

def RobotMove(distance, angle):
    #Implement code to move robot in desired way
    robot.iterativeTravel(angle,distance)
    return 1


def button_detect(image):
    #boundaries = [([0,125,125],[209,215,225])]
    ThresholdArray = [0,117,103,34,242,185]
    #for (lower,upper) in boundaries:
    #    lower = np.array(lower,dtype="uint8")
    #    upper = np.array(upper,dtype="uint8")
    lower = np.array([ThresholdArray[0],ThresholdArray[1],ThresholdArray[2]]) #np arrays for upper and lower thresholds
    upper = np.array([ThresholdArray[3], ThresholdArray[4], ThresholdArray[5]])
    mask = cv2.inRange(image,lower,upper)
    #output = cv2.bitwise_and(image,image,mask=mask)
    #cv2.imshow("images",output)
    return mask

def find_button(imgHSV):
    img2 = button_detect(imgHSV)
    boxcentrex= []
    boxcentrey= []
    area =[]
    print 'read imge'
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
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            print int(rect[0][0]),int(rect[0][1]),'centre'
            area.append(contourarea)
            boxcentrex.append(int(rect[0][0]))
            boxcentrey.append(int(rect[0][1]))
            cv2.drawContours(imgHSV,[approxcontour],0,(0,0,255),2)
            cv2.circle(imgHSV, (int(rect[0][0]), int(rect[0][1])), 5, (0,0,255),-1)

    print boxcentrex,boxcentrey
    #print 'boxcentrex',boxcentrex[0],boxcentrex[1],'boxcentrey',boxcentrey[0],boxcentrey[1]
    print 'area', area
    cv2.imshow("camera", imgHSV)
    return boxcentrex

def button_routine():
    img= vs.read()
    #cv2.imshow('img',img)
    #cv2.waitKey(1000)
    imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    xcord = find_button(imgHSV)
    return xcord


def stopcamera():
    cv2.destroyAllWindows()
    #print vs.stop()
    print 'Camera Stopped '

def QRDetect(image):
    scanner = zbar.ImageScanner()

    # configure the reader
    scanner.parse_config('enable')
    # obtain image data
    #gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY,dstCn=0)
    pil = Image.fromarray(image)
    width, height = pil.size
    raw = pil.tobytes()
    # wrap image data
    image = zbar.Image(width, height, 'Y800', raw)
    # scan the image for barcodes
    scanner.scan(image)

    # extract results
    for symbol in image:
        # do something useful with results
        if symbol.data == "None":
            print "Data Not read"
            return 0
        else:
            print symbol.data
            parsed_json = json.loads(symbol.data)
            return parsed_json
            #return symbol.data

def QR_Read():
    #qrcamera = cv2.VideoCapture(picamera)
    #ret, im = qrcamera.read()
    #Release camera
    #frcamera.release()
    time.sleep(1)
    im =  vs.read()
    im =  vs.read()
    im =  vs.read()
    im =  vs.read()
    imG = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    cv2.imshow('QR_Code',imG)
    cv2.waitKey(2000)
    json_data = QRDetect(imG)
    if(json_data != 0):
        print json_data
        return 1
    else:
        return 0


'''
GrayObjects = (0,132,124,209,232,223)#Red
while 1:
    Find_red_circles(GrayObjects)
    time.sleep(1)
'''
