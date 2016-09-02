   
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
#import neatoCom as robot
import serial
import RPi.GPIO as GPIO
import sys
import zbar
from PIL import Image
import json
from sys import argv


DisplayImage = True

#Find Circles
Contour_area_find_circles = 400
Approx_poly_dp_arc= 0.01
approx_cnt_dimen = 8

#Rect_in_Find_Circ
Approx_poly_dp_arc_rect_high = 0.08
Diatnce_aprox_value = 6


#Find Button
RedObjects_low = (0,100,100,10,255,255)#Red Low
RedObjects_high = (160,100,100,179,255,255)#Red High


Target_Green_threshold = [25,103,98,129,178,189]


Contr_Area_button_min = 2500
Contr_Area_target_min = 2500



print "Starting OpenCV"
#unified Pi camera+ USB
picamera = 0

vs = VideoStream(usePiCamera = picamera > 0 ).start()


if DisplayImage is True:
    cv2.namedWindow("camera", 0)
    cv2.namedWindow("output", 0)
    print  "Creating OpenCV windows"
    #cv2.waitKey(50)
    cv2.resizeWindow("camera", 640,480) 
    cv2.resizeWindow("output", 640,480) 
    print  "Resizing OpenCV windows"
    #cv2.waitKey(50)
    cv2.moveWindow("camera", 400,30)
    cv2.moveWindow("output", 1100,30)
    print  "Moving OpenCV window"
    cv2.waitKey(50)

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

def FindSymbol(ThresholdArray_low,ThresholdArray_high):
    TargetData = -1
    SymbolFound = -1
    vmfound = -1
    time.sleep(0.1)#let image settle
    frame = vs.read()
    frame = vs.read()
    frame = vs.read()
    frame = vs.read()
    frame = vs.read()
    img = frame.copy()
    imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV) #convert img to HSV and store result in imgHSVyellow

    #Threshold the lower Red
    lower_1 = np.array([ThresholdArray_low[0],ThresholdArray_low[1],ThresholdArray_low[2]]) #np arrays for upper and lower thresholds
    upper_1 = np.array([ThresholdArray_low[3], ThresholdArray_low[4], ThresholdArray_low[5]])
    imgthreshed_1 = cv2.inRange(imgHSV, lower_1, upper_1) #threshold imgHSV
    #Threshold the higher Red
    lower_2 = np.array([ThresholdArray_high[0],ThresholdArray_high[1],ThresholdArray_high[2]]) #np arrays for upper and lower thresholds
    upper_2 = np.array([ThresholdArray_high[3], ThresholdArray_high[4], ThresholdArray_high[5]])
    imgthreshed_2 = cv2.inRange(imgHSV, lower_2, upper_2) #threshold imgHSV

    cv.AddWeighted(imgthreshed_1,1.0,imgthreshed_2,1.0,0.0,img_thresh)

    _,contours, hierarchy = cv2.findContours(img_thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)  
    
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




def Find_red_circles(ThresholdArray_low,ThresholdArray_high):
    #time.sleep(0.5)
    TargetData = -1
    SymbolFound = -1
    vmfound = -1
    time.sleep(0.1)#let image settle
    frame = vs.read()
    frame = vs.read()
    frame = vs.read()
    frame = vs.read()
    img = frame.copy()
    imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV) #convert img to HSV and store result in imgHSVyellow

    #Threshold the lower Red
    lower_1 = np.array([ThresholdArray_low[0],ThresholdArray_low[1],ThresholdArray_low[2]]) #np arrays for upper and lower thresholds
    upper_1 = np.array([ThresholdArray_low[3], ThresholdArray_low[4], ThresholdArray_low[5]])
    imgthreshed_1 = cv2.inRange(imgHSV, lower_1, upper_1) #threshold imgHSV
    #Threshold the higher Red
    lower_2 = np.array([ThresholdArray_high[0],ThresholdArray_high[1],ThresholdArray_high[2]]) #np arrays for upper and lower thresholds
    upper_2 = np.array([ThresholdArray_high[3], ThresholdArray_high[4], ThresholdArray_high[5]])
    imgthreshed_1 = cv2.inRange(imgHSV, lower_2, upper_2) #threshold imgHSV
    
    cv.AddWeighted(imgthreshed_1,1.0,imgthreshed_2,1.0,0.0,img_thresh)
    cv2.imshow("output",  img_thresh)
    cv2.waitKey(5)

    _,contours, hierarchy = cv2.findContours(img_thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)  

    for x in range (len(contours)):
        contourarea = cv2.contourArea(contours[x]) #get area of contour
        #print 'contourarea',contourarea
        if contourarea > Contour_area_find_circles: #Discard contours with a small area as this may just be noise
            arclength = cv2.arcLength(contours[x], True)
            approxcontour = cv2.approxPolyDP(contours[x], Approx_poly_dp_arc * arclength, True) #Approximate contour to find square objects
            #print 'dimensions', len(approxcontour)
            if len(approxcontour) >= approx_cnt_dimen: #if approximated contour has 4 corner points
                
                rect = cv2.minAreaRect(contours[x])
                #print rect
                boxcentrex = int(rect[0][0])
                boxcentrey = int(rect[0][1])
                #cv2.drawContours(img,[approxcontour],0,(0,0,255),2)

                #############
                #For finding the distance of rectangle
                #############
                
                approxcontour = cv2.approxPolyDP(contours[x], Approx_poly_dp_arc_rect_high * arclength, True) #Approximate contour to find square objects
                #print 'dimensions', len(approxcontour)
                if len(approxcontour) == 4: #if approximated contour has 4 corner points
                    vmfound = 1
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
                    Distance = (640.00*Diatnce_aprox_value)/LongestSide #focal length x Actual Border width / size of Border in pixels
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
                        cv2.drawContours(img,[approxcontour],0,(0,0,255),2)
                        print TargetData
                        break
                            
    cv2.imshow("camera", img)            

    return TargetData



#########################################################################
##
## Functions for Circles
##
#########################################################################    
'''
def RobotMove(distance, angle):
    #Implement code to move robot in desired way
    robot.iterativeTravel(angle,distance)
    return 1
'''

def button_detect(image, ThresholdArray):
    lower = np.array([ThresholdArray[0],ThresholdArray[1],ThresholdArray[2]]) #np arrays for upper and lower thresholds
    upper = np.array([ThresholdArray[3], ThresholdArray[4], ThresholdArray[5]])
    mask = cv2.inRange(image,lower,upper)
    return mask



def find_button(imgHSV):
    boxcentrex= []
    boxcentrey= []
    area =[]
    #'''
    img2 = button_detect(imgHSV, Button_Red_threshold)

    #Threshold the lower Red
    lower_1 = np.array([RedObjects_low[0],RedObjects_low[1],RedObjects_low[2]]) #np arrays for upper and lower thresholds
    upper_1 = np.array([RedObjects_low[3], RedObjects_low[4], ThresholdArray_low[5]])
    imgthreshed_1 = cv2.inRange(imgHSV, lower_1, upper_1) #threshold imgHSV
    #Threshold the higher Red
    lower_2 = np.array([RedObjects_high[0],RedObjects_high[1],RedObjects_high[2]]) #np arrays for upper and lower thresholds
    upper_2 = np.array([RedObjects_high[3], RedObjects_high[4], RedObjects_high[5]])
    imgthreshed_2 = cv2.inRange(imgHSV, lower_2, upper_2) #threshold imgHSV

    cv.AddWeighted(imgthreshed_1,1.0,imgthreshed_2,1.0,0.0,img_thresh)

    print ' checking the button'
    _,contours, hierarchy = cv2.findContours(img_thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for x in range (len(contours)):
        contourarea = cv2.contourArea(contours[x]) #get area of contour
        if contourarea > Contr_Area_button_min: #Discard contours with a small area as this may just be noise
            arclength = cv2.arcLength(contours[x], True)
            approxcontour = cv2.approxPolyDP(contours[x], 0.08 * arclength, True)
            if len(approxcontour) == 4:
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
    #'''
    img2 = button_detect(imgHSV, Target_Green_threshold)
    print 'Checking Target'
    _,contours, hierarchy = cv2.findContours(img2,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for x in range (len(contours)):
        contourarea = cv2.contourArea(contours[x]) #get area of contour
        if contourarea > Contr_Area_target_min: #Discard contours with a small area as this may just be noise
            arclength = cv2.arcLength(contours[x], True)
            approxcontour = cv2.approxPolyDP(contours[x], 0.08 * arclength, True)
            if len(approxcontour) == 4:
                    
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
    #'''

    
    print 'boxcentrex',boxcentrex,'boxcentrey',boxcentrey
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
    if(json_data != None):
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
