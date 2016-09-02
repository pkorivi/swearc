import cv2
import numpy as np
from pyimagesearch.transform import four_point_transform
import time
import math
import SWEARCOpenCV
import neatoCom as robot
import sonar
import sys
import RPi.GPIO as GPIO
import serial
import pprint,os
import arduinoCom
#import circles as button

robotstate = ['start','SearchingTarget','NoTargetAround', 'MovingTowardsTarget','Missed_Target','Obstacle_encountered', 'Within_100cm',\
             'Within_30cm', 'Button_Routine','Button_pressed', 'Button_Missed', 'Reading_QR','QR_error','Task_Finished']
list(enumerate(robotstate))

Run = False
button_pressed = False
print 'To run the robot Should be replaced by switch'
arduino = arduinoCom.Arduino()
Thresh_head_pan = 4 #angle
Target_within = 100 #cm
Thresh_Dist_Target = 60#cm Max distance from target
Pixel_Diff_h_w = 10 #pixels
Alighment_dist = 100 #mm
Alignment_Angle = 60 #angle
x_cordi_difference = 10 # pixels
Robot_Move_dist = 200 #mm
No_target_angle =10 #angle
NO_target_loop_cnt = 36 #6*60 = 360

#Button_Move to target
Forward_move_target_thresh = 50
check_button_samples = 7
check_button_angle = 10


#robotstate = 'Reading_QR' 
#robotstate = 'Within_30cm'
robotstate = 'start'

t_sleep_0_5 = 0.5
t_sleep_1_0 = 1.0
t_sleep_1_5 = 1.5
t_sleep_2_0 = 2.0
t_sleep_3_0 = 3.0
t_sleep_4_0 = 4.0
t_sleep_9_0 = 9.0


RedObjects_low = (0,100,100,10,255,255)#Red Low
RedObjects_high = (160,100,100,179,255,255)#Red High

#Interrupt Routines
def interrupt_start(channel1):
    print 'Run Start Routine'
    global Run
    Run = True
    print Run
    

def interrupt_emergency(channel1):
    print 'Emergency Stop'
    RobotMove(0,0)
    GPIO.cleanup()
    robot.closeSerial()
    global Run
    Run = False
    sys.exit('Emergency Stop')
    

def interrupt_N(channel1):
    pass

def interrupt_E(channel1):
    pass

def interrupt_W(channel1):
    pass

def interrupt_S(channel1):
    pass

def interrupt_aurdino(channel1):
    pass

def interrupt_button_press(channel1):
    global button_pressed
    button_pressed = True
    global robotstate
    robotstate = 'Button_pressed'



###################################
#  PIN CONFIGURATION
###################################

GPIO.setmode(GPIO.BCM)
#Start and Emergency Stop
GPIO_Start = 23
GPIO_Emergency = 24

#Buttons for Task 2
GPIO_N = 5
GPIO_E = 6
GPIO_W = 13
GPIO_S = 19

#Aurdino Interrupt
GPIO_Aurdino = 26

#Button for press detcetion
GPIO_Button_press = 25

#Configured as pullup, Input
GPIO.setup(GPIO_Start,GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(GPIO_Emergency,GPIO.IN, pull_up_down = GPIO.PUD_UP)

GPIO.setup(GPIO_N,GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(GPIO_E,GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(GPIO_W,GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(GPIO_S,GPIO.IN, pull_up_down = GPIO.PUD_UP)

GPIO.setup(GPIO_Button_press,GPIO.IN, pull_up_down = GPIO.PUD_UP)

GPIO.setup(GPIO_Aurdino,GPIO.IN, pull_up_down = GPIO.PUD_UP)

#Interrupt Events
GPIO.add_event_detect(GPIO_Start, GPIO.FALLING, callback = interrupt_start,\
                      bouncetime = 2000)
GPIO.add_event_detect(GPIO_Emergency, GPIO.FALLING, callback = interrupt_emergency,\
                      bouncetime = 2000)
GPIO.add_event_detect(GPIO_N, GPIO.FALLING, callback = interrupt_N,\
                      bouncetime = 2000)
GPIO.add_event_detect(GPIO_E, GPIO.FALLING, callback = interrupt_E,\
                      bouncetime = 2000)
GPIO.add_event_detect(GPIO_W, GPIO.FALLING, callback = interrupt_W,\
                      bouncetime = 2000)
GPIO.add_event_detect(GPIO_S, GPIO.FALLING, callback = interrupt_S,\
                      bouncetime = 2000)
GPIO.add_event_detect(GPIO_Aurdino, GPIO.FALLING, callback = interrupt_aurdino,\
                      bouncetime = 2000)

GPIO.add_event_detect(GPIO_Button_press, GPIO.FALLING, callback = interrupt_button_press,\
                      bouncetime = 2000)



#Switch case to implement state Machines
class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration
    
    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args: # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False

def GetData():
    sonar = arduino.getSonar()
    return sonar

def AlignToTarget():
    print 'Aligning to Target'
    #while True:
    TargetData = CheckForTarget(1) #Check 3 times to see if target is still there
    if TargetData == -1:
        print " Lost Target "
        return -1
    else:#If target is still there, turn robot to face target
        HeadAngles = LookAtTarget(TargetData[0], TargetData[1])
        HeadPanAngle = HeadAngles[0]
        HeadTiltAngle = HeadAngles[1]
        print 'HeadPanAngle', HeadPanAngle 
        if abs(HeadPanAngle) < Thresh_head_pan: #When robot is looking at target, if head angle is less than 4 degrees either way
                                      #then target is dead ahead
            return 1 #if target has been found and robot is now facing target, return 1
        else: 
            print  "Target NOT ahead - Adjusting Heading"
            TurnToTarget(HeadPanAngle, 3) #Turn to face target
    return 1


def LookAtTarget(X,Y):

    print "Look at target : Checking the X and Y cam angles"
    HeadAngles = []
    XDist = X - 320.00
    XCamAngle = math.atan(XDist/640.00)
    YDist = 240.00 - Y
    YCamAngle = math.atan(YDist/640.00)
    HeadTiltAngle = math.degrees(YCamAngle)
    HeadPanAngle =  math.degrees(XCamAngle)
    HeadAngles.append(HeadPanAngle)
    HeadAngles.append(HeadTiltAngle)
    return HeadAngles

def TurnToTarget(TurnAngle, speed):
    print "Turning to face Target"
    if TurnAngle > 0:
        print "Turn Right"
        RobotData = RobotMove(0,TurnAngle,) 
    elif TurnAngle < 0:
        print "Turn Left"
        RobotData = RobotMove(0, TurnAngle)

def RobotMove(distance, angle):
    sleep = t_sleep_2_0
    if (distance != 0):
        if(distance<250):
            sleep = t_sleep_2_0
        elif (distance<500):
            sleep = t_sleep_3_0+t_sleep_0_5
        else:
            sleep = t_sleep_9_0

    if (angle != 0):
        if(angle<5):
            sleep = t_sleep_0_5
        elif (angle<25):
            sleep = t_sleep_1_5
        elif (angle<61):
            sleep = t_sleep_1_5
        else:
            sleep = t_sleep_2_0+t_sleep_0_5

    robot.iterativeTravel(angle,distance,sleep)
    return 1

def MoveToTarget():
    print "Moving to Target"
    #while True:
    TargetData = CheckForTarget(2)#Capture image and check for symbol
    if TargetData == -1:
        print "No Target In Image"
        return -1 #if no target is found, return -1 immediately
    else: #Target is there as expected
        print  "Target found in MoveToTarget"
        Result = AlignToTarget()
        print 'Aligning result ',Result
        if Result ==1:
            print "Moving Forward"
            RobotData = RobotMove(Robot_Move_dist,0)
            dist = GetData()
            if dist[2] <= Forward_move_target_thresh:
                return 1
            else:
                return 0xFF   
        else: #Target Found But Need to move more forward
             return 0xFF


'''
def MoveToTarget():
    print "Moving to Target"
    while True:
        TargetData = CheckForTarget(2)#Capture image and check for symbol
        if TargetData == -1:
            print "No Target In Image"
            return -1 #if no target is found, return -1 immediately
        else: #Target is there as expected
            print  "Target found in MoveToTarget"
            if TargetData[2] < Target_within:
                print "Target within ", Target_within
                if TargetData[2] < 30: #if target is too close
                    print "Target too close - Reversing"
                    RobotData = RobotMove(-100,0)
                if TargetData[5] > -Pixel_Diff_h_w and TargetData[5] < Pixel_Diff_h_w: #Target ahead
                    print "Target straight Ahead !!"
                    attarget = False
                    while attarget == False:
                        RobotData = GetData()
                        print RobotData,'RobotData'
                        if (RobotData) > Thresh_Dist_Target:
                            RobotData = RobotMove(150,0)
                        else:
                            attarget = True
                            print 'target Reached'
                    return 1
                else:
                    if TargetData[4] == "LEFT":
                        print 'Turn left'
                        RobotData = RobotMove(0,-Alignment_Angle)
                        RobotData = RobotMove(Alighment_dist,0)
                        RobotData = RobotMove(0,Alignment_Angle)
            
                    else:
                        print 'Turning right'
                        RobotData = RobotMove(0,Alignment_Angle)
                        RobotData = RobotMove(Alighment_dist,0)
                        RobotData = RobotMove(0,-Alignment_Angle)
                    
                    Result = AlignToTarget()
                    if Result == -1:  
                        return -1
            #else for target >100cm        
            else:
                print "Target further than 100cm"
                Result = AlignToTarget()
                print 'Aligning result ',Result
                if Result ==1:
                    print "Moving Forward"
                    RobotData = RobotMove(Robot_Move_dist,0)
                else:
                    return -1
                    
'''

def CheckForTarget(tries):
    print 'Check for Symbol'
    #tries = 3
    for x in range (0,tries):
        #TargetData = SWEARCOpenCV.FindSymbol(GrayObjects)
        TargetData = SWEARCOpenCV.Find_red_circles(RedObjects_low,RedObjects_high)
    print 'CFS : Target data', TargetData
    if TargetData != -1:#Target present          
        if TargetData[3] == 1: #if its the correct target type
            return TargetData #return straight away if correct symbol found
    return -1


def ScanForTarget():
    returndata = -1
    print "Scanning for Target"
    TargetData = CheckForTarget(1)
    print 'Targetata : ',TargetData 
    #Capture image and check for symbol
    if TargetData == -1:
        print " Not good -No Image in Vicinity"
    else:
        print "I found my Crush"
        Aligned = AlignToTarget()
        if Aligned == 1:
            return 1
    #Nothing found - Dump the stuff.   
    return returndata


###############################
## MAIN ROBOT CODE
###############################

arduino.setServos(30,30,30)
print "Mission: Robot Navigation about to Start"
while True:
    while Run is True:
        #print "Loop"
        for case in switch(robotstate):
			if case('start'):
				print 'Start - caliberate'
				robotstate = 'SearchingTarget'
				command = "espeak -ven+m1 -a 200 -p 30 -s 150 -g 12 'Its time to FInd Vending Machine' 2>/dev/null > /dev/null"
                                os.system(command)
                                last = 0
                                #RobotMove(1600,0)
                                #time.sleep(4)				
				break
			if case('SearchingTarget'):
				print 'SearchingTarget'
				check_button_samples = 7
                                check_button_angle = 10
                                RobotMove(0,(math.floor(check_button_samples/2))*check_button_angle)
				for x in range (0,check_button_samples):
                                    print 'Scanning Angle of Robot:', x*check_button_angle
                                    Result = ScanForTarget()
                                    if Result == -1:
                                            print "No Target found from scan"
                                            #turn 90 degrees to the left
                                            RobotData = RobotMove(0,check_button_angle)  # Distnace, Angle no sonar or IR threshold so move always completes
                                            robotstate = 'NoTargetAround'
                                    else:
                                            print "Target Aquired"
                                            TargetAquired = True
                                            robotstate = 'MovingTowardsTarget'
                                            break
                                if Result == -1:
                                    RobotMove(0,-((math.floor(check_button_samples/2))*check_button_angle+check_button_angle))
                                
				break #break for searchingtarget
			if case('NoTargetAround'):
				print 'NoTargetAround'
				#RobotData = RobotMove(0,90)
				RobotData = RobotMove(500,0)
				#RobotData = RobotMove(0,-90)
				robotstate = 'SearchingTarget'
				break
			if case('MovingTowardsTarget'):
				print 'MovingTowardsTarget'
				result = MoveToTarget()
				if result == 1:
                                    robotstate = 'Within_30cm'
                                    print "Reached Robot"
                                elif result == 0xFF:
                                    pass
                                else:
                                    print "Lost Myself - Need something else"
                                    #Move to a different location and scan again here
                                    robotstate = 'Missed_Target'
				break
			if case('Missed_Target'):
				print 'Missed_Target'
				#start again from initial
				robotstate = 'SearchingTarget'
				break
			if case('Obstacle_encountered'):
				print 'Obstacle_encountered' 
				break
			if case('Within_100cm'):
				print 'Within_100cm'
				break
			if case('Within_30cm'):
                                print 'Within_30cm'
				#check for Button
				robotstate = 'Button_Routine'
				cv2.destroyAllWindows()
				break
			if case('Button_Routine'):
				print 'Button_Routine'
				xcordi = SWEARCOpenCV.button_routine()
				if len(xcordi)>=2:
                                    if (xcordi[0]-xcordi[1])>15:                                        #ARM IS TO RIGHT
                                        RobotMove(0,1)
                                        print 'arm left'
                                    elif (xcordi[0]-xcordi[1])<-15:
                                        RobotMove(0,-1)
                                        print 'arm right'
                                    else:
                                        RobotMove(50,0)                                        
                                        print 'move forward'
                                        RobotData = GetData()
                                        print RobotData,'RobotData'
                                        print 'GPIO',GPIO.input(GPIO_Button_press)
                                        if (RobotData) < 40:
                                            while(button_pressed == False):
                                                arduino.setServos(0,0,0)
                                                RobotMove(15,0)
                                            robotstate = 'Button_pressed'
                                else:
                                    robotstate = 'Button_Missed'
				break
			if case('Button_pressed'):
				print 'Button_pressed'
				print 'Moving Back to Read QR Code'
				command = "espeak -ven+m1 -a 200 -p 30 -s 150 -g 12 'Button Pressed, Time to read QR' 2>/dev/null > /dev/null"
                                os.system(command)
                                last = 0
                                time.sleep(4)
                                RobotMove(-1600,0)
				robotstate = 'Reading_QR'
				break
			if case('Button_Missed'):
				print 'Button_Missed'
				RobotMove(10,0)
				robotstate = 'Button_Routine'
				break
			if case('Reading_QR'):
				print 'Reading_QR'
				time.sleep(5)
				qr_ret = SWEARCOpenCV.QR_Read()
				if (qr_ret == 1):
                                    print 'QR Success'
                                    command = "espeak -ven+m1 -a 200 -p 30 -s 150 -g 12 'QR_Read' 2>/dev/null > /dev/null"
                                    os.system(command)
                                    last = 0
                                    time.sleep(3)
                                    robotstate = 'Task_Finished'
                                else:
                                    robotstate = 'QR_error'
				break
			if case('QR_error'):
				print 'QR_error'
				robotstate = 'Task_Finished'
				break
                        if case('Task_Finished'):
				print 'Task Fnished'
				command = "espeak -ven+m1 -a 200 -p 30 -s 150 -g 12 'Task Finisged, Bye See You soon' 2>/dev/null > /dev/null"
                                os.system(command)
                                last = 0
                                time.sleep(4)
                                GPIO.cleanup()
				robot.closeSerial()
				sys.exit('Button ROutine not defined')
				break
			if case():
				print 'Default_ Dont know what to do'
				break

        print '#end#'

