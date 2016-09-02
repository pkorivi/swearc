import cv2
import numpy as np
import time
import math
import neatoCom as robot
import RPi.GPIO as GPIO
import neatoCom as robot
import sonar
import sys
import serial
import time
from collections import Counter
import math
import pprint,os

GPIO.setmode(GPIO.BCM)
GPIO_Interrupt = 21
GPIO_sonar2 = 20
GPIO.setup(GPIO_sonar2,GPIO.IN, pull_up_down = GPIO.PUD_UP)      # Echo
#Configured as pullup, Input
GPIO.setup(GPIO_Interrupt,GPIO.IN, pull_up_down = GPIO.PUD_UP)

def interrupt_callback(channel1):
    #RobotMove(-30,0) #MOve back
    #RobotMove(0,2)#MOve right by 2 degree
    print 'Check what to do if we are about to hit in right side into the chairs'
    #command = "espeak -ven+m1 -a 200 -p 30 -s 150 -g 12 'Hello I am Moose, Please follow me' 2>/dev/null > /dev/null"
    #os.system(command)
    #last = 0
    

GPIO.add_event_detect(GPIO_Interrupt, GPIO.FALLING, callback = interrupt_callback,\
                      bouncetime = 300)
'''
while True:
    print 'Robot whats happening'
    time.sleep(0.1)
    print GPIO.input(GPIO_sonar2)
    
'''

t_sleep_0_5 = 0.5
t_sleep_1_0 = 1.0
t_sleep_1_5 = 1.5
t_sleep_2_0 = 2.0
t_sleep_3_0 = 3.0
t_sleep_4_0 = 4.0
t_sleep_8_0 = 8.0
t_sleep_10_0 = 10.0

Thresh_head_pan = 4 #angle
Target_within = 150 #cm
Thresh_Dist_Target = 60#cm Max distance from target
Pixel_Diff_h_w = 10 #pixels
Alighment_dist = 100 #mm
Alignment_Angle = 60 #angle
x_cordi_difference = 10 # pixels
Robot_Move_dist = 200 #mm
No_target_angle =60 #angle
NO_target_loop_cnt = 6 #6*60 = 360

#Find Circles
Contour_area_find_circles = 400
Approx_poly_dp_arc= 0.01
approx_cnt_dimen = 8

#Rect_in_Find_Circ
Approx_poly_dp_arc_rect_high = 0.08
Diatnce_aprox_value = 5


#Find Button
Button_Red_threshold = [0,132,124,209,232,223]
Target_Green_threshold = [32,63,106,84,210,167]
Contr_Area_button_min = 2500
Contr_Area_target_min = 2500
def RobotMove(distance, angle, sleep):
    #Implement code to move robot in desired way
    robot.iterativeTravel(angle,distance,sleep)
    return 1
time.sleep(2)


RobotData = RobotMove(0,-60,3)
RobotData = RobotMove(150,0,3)
RobotData = RobotMove(0,60,3)
                

'''
RobotData = RobotMove(0,1,0.5)
RobotData = RobotMove(0,60,1.5)
RobotData = RobotMove(0,1,0.5)
RobotData = RobotMove(0,60,1.5)
'''
dist = 0
t= 1.5
angle = 30

'''
RobotData = RobotMove(0,-20,t)
RobotData = RobotMove(-800,0,t)
RobotData = RobotMove(0,50,t)
RobotData = RobotMove(dist,angle,t)
RobotData = RobotMove(-dist,-angle,t)
RobotData = RobotMove(dist,angle,t)
RobotData = RobotMove(-dist,-angle,t)
'''
#RobotData = RobotMove(0,-60,3)

'''
print 'Forward'
RobotMove(100,0)
print 'Backward'
RobotMove(-100,0)
print '90 degree'
RobotMove(0,90)
print '90 degree'
RobotMove(0,-90)
print 'Done'
'''




#'''
'''
#For CIrcles

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
