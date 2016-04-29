import cv2
import numpy as np
#from colorama import init,Fore
from pyimagesearch.transform import four_point_transform
import time
import math
import SWEARCOpenCV
import neatoCom as robot

symbol = 'VM'
robotstates = ['SearchingTarget', 'MovingTowardsTarget','Missed_Target','Obstacle_encountered', 'Within_100cm',\
             'Within_30cm', 'Button_Routine','Button_pressed', 'Button_Missed', 'Reading_QR','QR_error']

BrownObjects = [22,17,18,101,255,105]
    
def GetData():
    return robot.getScan()

def AlignToTarget():
    print 'Aligning to Target'
    while True:
        TargetData = CheckForTarget(1) #Check 3 times to see if target is still there
        if TargetData == -1:
            print " Lost Target "
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
        #RobotData = HeadMove(HeadPanAngle,HeadTiltAngle, 8) #Centre head
        TargetData = CheckForTarget(3)#Capture image and check for symbol
        if TargetData == -1:
            print "No Target In Image"
            return -1 #if no target is found, return -1 immediately
        else: #Target is there as expected
            print  "Target found in MoveToTarget"
            if TargetData[2] < 100:
                print "Target within 100cm"
                if TargetData[2] < 25: #if target is too close
                    print "Target too close - Reversing"
                    RobotData = RobotMove(-20,0)
                    #RobotData = RobotMove(ROBOTREVERSE, 30, AutoSpeed, 0, 255)#back up a bit
                if TargetData[5] > 0.96 and TargetData[5] < 1.04: #Target ahead
                    print "Target straight Ahead !!"
                    attarget = False
                    while attarget == False:
                        RobotData = GetData()
                        #distance_ahead = min(RobotData)
                        if (RobotData/10) > 30:
                            RobotData = RobotMove(20,0)
                            '''
                            print  "Sonar in MoveToTarget - " + str(RobotData[5])
                            print "LeftIR -", RobotData[0]
                            print "CentreIR -", RobotData[1]
                            print "RightIR -", RobotData[2]
                            '''
                        else:
                            attarget = True
                            print 'target Reached'
            
                    #RobotData = RobotMove(ROBOTRIGHT, 200/TurnRatio, AutoSpeed, 0, 255)
                    #RobotData = RobotMove(ROBOTREVERSE, 30, AutoSpeed, 5, 80)
                    return 1
                else:
                    if TargetData[4] == "LEFT":

                        RobotData = RobotMove(0,-10)
                        RobotData = RobotMove(10,0)
                        RobotData = RobotMove(0,10)
                        '''
                        RobotData = RobotMove(ROBOTRIGHT, 10, AutoSpeed, 0, 255)
                        RobotData = RobotMove(ROBOTFORWARD, 30, AutoSpeed, 20, 100)
                        RobotData = RobotMove(ROBOTLEFT, 10, AutoSpeed, 0, 255)
                        '''
                        Result = AlignToTarget()
                    elif TargetData[4] == "RIGHT":
                        '''
                        RobotData = RobotMove(ROBOTLEFT, 10, AutoSpeed, 0, 255)
                        RobotData = RobotMove(ROBOTFORWARD, 30, AutoSpeed, 20, 100)
                        RobotData = RobotMove(ROBOTRIGHT, 10, AutoSpeed, 0, 255)
                        '''
                        RobotData = RobotMove(0,10)
                        RobotData = RobotMove(10,0)
                        RobotData = RobotMove(0,-10)
                        Result = AlignToTarget()
                    else: #Target is head so just aligh
                        Result = AlignToTarget()

                    
            else:
                print "Target further than 100cm"
                Result = AlignToTarget()
                if Result ==1:
                    print "Moving Forward"
                    RobotData = RobotMove(20,0)
                    #RobotData = RobotMove(ROBOTFORWARD, 100, AutoSpeed, 10, 100) #
                    '''
                    if RobotData[6] < 100 and RobotData[7] < 100:
                        print "Obstacle encountered"
                        return -1
                    '''


def CheckForTarget(tries):
    print 'Check for Symbol'
    for x in range (0,tries):
        TargetData = SWEARCOpenCV.FindSymbol(BrownObjects)
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




print "Mission Robot Navigation abut to Start"
Run = True
symbol = 'VM'
while True:
    
    while Run is True:
        print "##################################################"
        print "     "
        TargetAquired = False
        for x in range (0,4):
            print 'Scanning Angle of Robot:', x*90 
            Result = ScanForTarget()
            if Result == -1:
                print "No Target found from scan"
                #turn 120 degrees to the left
                RobotData = RobotMove(0,90)  # Distnace, Angle no sonar or IR threshold so move always completes
            else:
                print "Target Aquired"
                TargetAquired = True
                break
        
        if TargetAquired is True:
            result = MoveToTarget()
            if result == 1:
                Run = False
                print "Mission Accomplished"
            else:
                print "Lost Myself - Need something else"
                #Move to a different location and scan again here
                Run = True
                print "Press button 0 to start"
         #time.sleep(4)
        print "########################"
        print '#end#'

