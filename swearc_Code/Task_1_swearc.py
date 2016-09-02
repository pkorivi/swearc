#import cv2
#import numpy as np
from pyimagesearch.transform import four_point_transform
import time
import math
import Opencv_task1
import neatoCom as robot
import sonar
import sys
import RPi.GPIO as GPIO
import serial
#import circles as button

robotstate = ['start','SearchingTarget','NoTargetAround', 'MovingTowardsTarget','Align_to_VM','Missed_Target','Move_to_Button', 'Within_100cm',\
             'Within_30cm', 'Button_Routine','Button_pressed', 'Button_Missed', 'Reading_QR','QR_error','Task_Finished']
list(enumerate(robotstate))

Run = True
print 'To run the robot Should be replaced by switch'

Thresh_head_pan = 4 #angle
Target_within = 100 #cm
Thresh_Dist_Target = 50#cm Max distance from target
Pixel_Diff_h_w = 10 #pixels
req_wh_ratio = (0.98,1.02)
Alighment_dist = 100 #mm
Alignment_Angle = 60 #angle
x_cordi_difference = 10 # pixels
Robot_Move_dist = 200 #mm
No_target_angle =60 #angle
NO_target_loop_cnt = 6 #6*60 = 360



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


#GrayObjects = [29,30,130,85,173,195]
GrayObjects = (0,119,90,194,185,146)#Red
BlueObjects = (60,60,60,168,215,215) #Blue
#GrayObjects = [0,0,124,186,60,160]
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
    return sonar.measure_mode()

def AlignToTarget(item):
    print 'Aligning to Target'
    while True:
        TargetData = CheckForTarget(1,item) #Check 3 times to see if target is still there
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
            sleep = t_sleep_3_0
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
            sleep = t_sleep_3_0
        else:
            sleep = t_sleep_2_0+t_sleep_0_5

    robot.iterativeTravel(angle,distance,sleep)
    return 1


def Move_parallel_VM():
    print "Moving Parallel to VM"
    TargetData = CheckForTarget(1, 'qrc_box')#Capture image and check for symbol
    if TargetData == -1:
        print "No Target In Image"
        return -1 #if no target is found, return -1 immediately
    else: #Target is there as expected
        print  "VM found in MoveParallelToVM"
        if TargetData[2] < 125:
            if TargetData[2] < 30: #if target is too close
                print "Target too close - Reversing"
                RobotData = RobotMove(-100,0)
            if TargetData[5] > req_wh_ratio[0] and TargetData[5] < req_wh_ratio[1]: #Target ahead
                print "Target straight Ahead !!"
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
                
                Result = AlignToTarget('qrc_box')
                if Result == -1:  
                    return -1
        else:
            Result = AlignToTarget('qrc_box')
            if Result == -1:  
                return -1
            else:
                if TargetData[4] == "LEFT":
                    print 'Turn left'
                    RobotData = RobotMove(0,-90)
                    RobotData = RobotMove(Alighment_dist,0)
                    RobotData = RobotMove(0,90)
        
                else:
                    print 'Turning right'
                    RobotData = RobotMove(0,Alignment_Angle)
                    RobotData = RobotMove(Alighment_dist,0)
                    RobotData = RobotMove(0,-Alignment_Angle)
                RobotMove(150,0)
                Result = AlignToTarget('qrc_box')
                if Result == -1:  
                    return -1
            
    return 0xFF          

def MoveToButton():
    print 'Move to Button'
    TargetData = CheckForTarget(1,'red_button')#Capture image and check for symbol
    if TargetData == -1:
        print "No Target In Image"
        return -1 #if no target is found, return -1 immediately
    else: #Target is there as expected
        print  "Button found in MoveToButton"
        if TargetData[2] < Target_within:
            print "Target within ", Target_within
            if TargetData[2] < 30: #if target is too close
                print "Target too close - Reversing"
                RobotData = RobotMove(-200,0)
            else:
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
        #else for target >100cm        
        else:
            print "Target further than 100cm"
            Result = AlignToTarget('red_button')
            if Result ==1:
                print "Moving Forward"
                RobotData = RobotMove(Robot_Move_dist,0)
            else:
                return -1
    return 0xFF




def CheckForTarget(tries, symbol):
    for x in range (0,tries):
        if symbol == 'qrc_box':
            print 'Check for Symbol VM'
            TargetData = Opencv_task1.FindSymbol(BlueObjects)
        elif symbol == 'red_button':
            print 'Check for Symbol Button'
            print GrayObjects
            TargetData = Opencv_task1.Find_red_circles(GrayObjects)
        else:
            print 'I cannot identify what you have mentioned'

        print 'CFS : Target data', TargetData
        if TargetData != -1:#Target present          
            if TargetData[3] == 1: #if its the correct target type
                return TargetData #return straight away if correct symbol found
    return -1


def ScanForTarget(item):
    returndata = -1
    print "Scanning for Target"
    TargetData = CheckForTarget(1, item)
    print 'Targetata : ',TargetData 
    #Capture image and check for symbol
    if TargetData == -1:
        print " Not good -No Image in Vicinity"
    else:
        print "I found my Crush"
        Aligned = AlignToTarget(item)
        if Aligned == 1:
            return 1
    #Nothing found - Dump the stuff.   
    return returndata


###############################
## MAIN ROBOT CODE
###############################

print "Mission: Robot Navigation about to Start"
search_item = 'red_button'
skip_align_vm = False
while True:
    while Run is True:
        time.sleep(1)
        #print "Loop"
        for case in switch(robotstate):
	    if case('start'):
		print 'Start - caliberate'
		robotstate = 'SearchingTarget'
		break
            if case('SearchingTarget'):
		print 'SearchingTarget'
                for x in range (0,NO_target_loop_cnt):
                    print 'Scanning Angle of Robot:', x*No_target_angle
                    if skip_align_vm == False:
                        Result = ScanForTarget('qrc_box')
                    else:
                        Result = ScanForTarget('red_button')
                    
                    if Result == -1:
                        print "No Target found from scan"
                        RobotData = RobotMove(0,No_target_angle)  # Distnace, Angle no sonar or IR threshold so move always completes
                        robotstate = 'NoTargetAround'
                    else:
                        print "Target Aquired"
                        TargetAquired = True
                        if skip_align_vm == False:
                            robotstate = 'Align_to_VM'
                        else:
                            robotstate = 'Move_to_Button'
                        break#break for loop
                break #break for searchingtarget
            if case('NoTargetAround'):
                print 'NoTargetAround'
                RobotData = RobotMove(0,-90)
                RobotData = RobotMove(300,0)
                RobotData = RobotMove(0,90)
                robotstate = 'SearchingTarget'
                break
            if case('Align_to_VM'): #Moving parallel to VM
		print 'Align_to_VM'
		result = Move_parallel_VM()
		if result == 1:
                    robotstate = 'Move_to_Button'
                    print "Done!!! ALigned to the VM"
                elif result == 0xFF:
                    pass
                else:
                    print "Lost Myself - Need something else"
                    #Move to a different location and scan again here
                    robotstate = 'Missed_Target'
		break
	    if case('Missed_Target'):
		print 'Missed_Target'
		robotstate = 'SearchingTarget'
		break
            if case('Move_to_Button'):
		print 'Move_to_Button' 
                result = MoveToButton()
                if result == 1:
                    robotstate = 'Within_30cm'
                    print "Reached Robot"
                elif result == 0xFF:
                    pass
                else:
                    print "Lost Myself - Need something else"
                    #Move to a different location and scan again here
                    robotstate = 'Missed_Target'
                    skip_align_vm = True
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
		xcordi = Opencv_task1.button_routine()
		if len(xcordi)==2:
                    if (xcordi[0]-xcordi[1])>15:   #ARM IS TO LEFT
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
                        if (RobotData) < 30:
                            robotstate = 'Button_pressed'
                else:
                    robotstate = 'Button_Missed'
		break
	    if case('Button_pressed'):
		print 'Button_pressed'
		print 'Moving back to read QR'
                RobotMove(-1300,0)
		robotstate = 'Reading_QR'
                break
	    if case('Button_Missed'):
		print 'Button_Missed'
		robotstate = 'Reading_QR'
		break
	    if case('Reading_QR'):
		print 'Reading_QR'                                
		qr_ret = Opencv_task1.QR_Read()
		if (qr_ret == 1):
                    print 'QR Success'
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
                GPIO.cleanup()
		robot.closeSerial()
		sys.exit('Button ROutine not defined')
		break
	    if case():
		print 'Default_ Dont know what to do'
		break

        print '#end#'

