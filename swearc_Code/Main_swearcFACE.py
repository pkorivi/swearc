import cv2
import numpy as np
#from colorama import init,Fore
from pyimagesearch.transform import four_point_transform
import time
import math
import SWEARCOpenCV
import neatoCom as robot
import sonar
import sys
import RPi.GPIO as GPIO
import serial

robotstate = ['start','SearchingTarget','NoTargetAround', 'MovingTowardsTarget','Missed_Target','Obstacle_encountered', 'Within_100cm',\
             'Within_30cm', 'Button_Routine','Button_pressed', 'Button_Missed', 'Reading_QR','QR_error','Task_Finished']
list(enumerate(robotstate))

GrayObjects = [38,66,40,136,255,127]

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

def AlignToTarget():
    print 'Aligning to Target'
    while True:
        TargetData = CheckForTarget(1) #Check 3 times to see if target is still there
        if TargetData == -1:
            print " Lost Target "
            return -1
        else:#If target is still there, turn robot to face target
            HeadAngles = LookAtTarget(TargetData[0], TargetData[1])
            HeadPanAngle = HeadAngles[0]
            HeadTiltAngle = HeadAngles[1]
            print 'HeadPanAngle', HeadPanAngle 
            if abs(HeadPanAngle) < 10: #When robot is looking at target, if head angle is less than 4 degrees either way
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
    #RobotData = HeadMove(HeadPanAngle,HeadTiltAngle, 8)
    #RobotData = RobotMove(0,HeadPanAngle) 
    HeadAngles.append(HeadPanAngle)
    HeadAngles.append(HeadTiltAngle)
    return HeadAngles

def TurnToTarget(TurnAngle, speed):
    print "Turning to face Target"
    if TurnAngle > 0:
        print "Turn Right"
        RobotData = RobotMove(0,TurnAngle) 
    elif TurnAngle < 0:
        print "Turn Left"
        RobotData = RobotMove(0, TurnAngle)

def RobotMove(distance, angle):
    #Implement code to move robot in desired way
    robot.iterativeTravel(angle,distance)
    return 1


def MoveToTarget():
    print "Moving to Target"
    while True:
        HeadPanAngle = 0
        HeadTiltAngle = 0
        TargetData = CheckForTarget(3)#Capture image and check for symbol
        if TargetData == -1:
            print "No Target In Image"
            return -1 #if no target is found, return -1 immediately
        else: #Target is there as expected
            print  "Target found in MoveToTarget"
            if TargetData[2] < 100:
                print "Target within 100cm"
                if TargetData[2] < 30: #if target is too close
                    print "Target too close - Reversing"
                    RobotData = RobotMove(-100,0)
                    #RobotData = RobotMove(ROBOTREVERSE, 30, AutoSpeed, 0, 255)#back up a bit
                if TargetData[5] > 0.98 and TargetData[5] < 1.02: #Target ahead
                    print "Target straight Ahead !!"
                    attarget = False
                    while attarget == False:
                        RobotData = GetData()
                        print RobotData,'RobotData'
                        if (RobotData) > 40:
                            RobotData = RobotMove(150,0)
                            '''
                            Result = AlignToTarget()
                            if Result == -1:  
                                return -1
                            print 'Change the code'
                            '''
                        else:
                            attarget = True
                            print 'target Reached'
                    return 1
                else:
                    if TargetData[4] == "LEFT":
                        print 'Turn left'
                        RobotData = RobotMove(0,-60)
                        RobotData = RobotMove(100,0)
                        RobotData = RobotMove(0,60)
            
                    else:
                        print 'Turning right'
                        RobotData = RobotMove(0,60)
                        RobotData = RobotMove(100,0)
                        RobotData = RobotMove(0,-60)
                    
                    Result = AlignToTarget()
                    if Result == -1:  
                        return -1
            #else for target >100cm        
            else:
                print "Target further than 100cm"
                Result = AlignToTarget()
                if Result ==1:
                    print "Moving Forward"
                    RobotData = RobotMove(200,0)
                else:
                    return -1
                    


#def CheckForTarget(tries):
#    print 'Check for Symbol'
#    for x in range (0,tries):
#        TargetData = SWEARCOpenCV.FindSymbol(GrayObjects)
#        print 'CFS : Target data', TargetData
#        if TargetData != -1:#Target present          
#            if TargetData[3] == 1: #if its the correct target type
#                return TargetData #return straight away if correct symbol found
#    return -1

def CheckForTarget(tries):
    print 'Check for Human'
    for x in range (0,tries):
        TargetData = SWEARCOpenCV.FindHuman(GrayObjects)
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


#########Need to be chnaged to a switch
Run = True
robotstate = 'start'
print "Mission: Robot Navigation about to Start"
while True:
    while Run is True:
        print "Loop"
        for case in switch(robotstate):
			if case('start'):
				print 'Start - caliberate'
				robotstate = 'SearchingTarget'
				break
			if case('SearchingTarget'):
				print 'SearchingTarget'
				for x in range (0,6):
                                    print 'Scanning Angle of Robot:', x*60 
                                    Result = ScanForTarget()
                                    if Result == -1:
                                            print "No Target found from scan"
                                            #turn 90 degrees to the left
                                            RobotData = RobotMove(0,60)  # Distnace, Angle no sonar or IR threshold so move always completes
                                            robotstate = 'NoTargetAround'
                                    else:
                                            print "Target Aquired"
                                            TargetAquired = True
                                            robotstate = 'MovingTowardsTarget'
                                            break
				break #break for searchingtarget
			if case('NoTargetAround'):
				print 'NoTargetAround'
				RobotData = RobotMove(0,90)
				RobotData = RobotMove(300,0)
				RobotData = RobotMove(0,-90)
				robotstate = 'SearchingTarget'
				break
			if case('MovingTowardsTarget'):
				print 'MovingTowardsTarget'
				result = MoveToTarget()
				if result == 1:
                                    robotstate = 'Within_30cm'
                                    print "Reached Robot"
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
				break
			if case('Button_Routine'):
				print 'Button_Routine'
				robotstate = 'Task_Finished'
				break
			if case('Button_pressed'):
				print 'Button_pressed'
				break
			if case('Button_Missed'):
				print 'Button_Missed'
				break
			if case('Reading_QR'):
				print 'Reading_QR'
				Run = False
				break
			if case('QR_error'):
				print 'QR_error'
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

