import cv2
import numpy as np
from colorama import init,Fore
from pyimagesearch.transform import four_point_transform
import time
import SWEARCOpenCV

BrownObjects = [5,5,23,225,119,170]

def TurnToTarget(TurnAngle, speed):
    print "Turning to face Target"
    if TurnAngle > 0:
        print "Turn Right"
        #RobotData = RobotMove(0,TurnAngle) 
    elif TurnAngle < 0:
        print "Turn Left"
        #RobotData = RobotMove(0, TurnAngle)
    

def AlignToTarget(symbol):
    while True:
        TargetData = CheckForTarget(Symbol,3) #Check 3 times to see if target is still there
        if TargetData == -1:
            print " Lost Target "
        else:#If target is still there, turn robot to face target
            HeadAngles = LookAtTarget(TargetData[0], TargetData[1])
            HeadPanAngle = HeadAngles[0]
            HeadTiltAngle = HeadAngles[1]
            if abs(HeadPanAngle) < 4: #When robot is looking at target, if head angle is less than 4 degrees either way
                                      #then target is dead ahead
                return 1 #if target has been found and robot is now facing target, return 1
            else: 
                print (Fore.BLUE + "Target NOT ahead - Adjusting Heading")
                TurnToTarget(HeadPanAngle, 3) #Turn to face target





def LookAtTarget(X,Y):

    print "Lookinf for Target"
    HeadAngles = []
    XDist = X - 320.00
    XCamAngle = math.atan(XDist/640.00)
    YDist = 240.00 - Y
    YCamAngle = math.atan(YDist/640.00)
    HeadTiltAngle = math.degrees(YCamAngle)
    HeadPanAngle =  math.degrees(XCamAngle)
    #RobotData = HeadMove(HeadPanAngle,HeadTiltAngle, 8)
    HeadAngles.append(HeadPanAngle)
    HeadAngles.append(HeadTiltAngle)
    return HeadAngles


    #Do Something
def RobotMove(distance, angle):
    #Implement code to move robot in desired way
    return 1


def MoveToTarget(symbol):
    print "Moving to Target"
    while True:
        HeadPanAngle = 0
        HeadTiltAngle = 0
        #RobotData = HeadMove(HeadPanAngle,HeadTiltAngle, 8) #Centre head
        TargetData = CheckForTarget(Symbol,3)#Capture image and check for symbol
        if TargetData == -1:
            print (Fore.BLUE + "No Target In Image")
            return -1 #if no target is found, return -1 immediately
        else: #Target is there as expected
            print (Fore.BLUE + "Target found in MoveToTarget")
            if TargetData[2] < 100:
                print "Target within 100cm"
                if TargetData[2] < 25: #if target is too close
                    print (Fore.BLUE + "Target too close - Reversing")
                    RobotData = RobotMove(ROBOTREVERSE, 30, AutoSpeed, 0, 255)#back up a bit
                if TargetData[5] > 0.98 and TargetData[5] < 1.02: #Target ahead
                    print "Target Reached!!"
                    attarget = False
                    while attarget == False:
                        RobotData = GetData()
                        if RobotData[5] > 20:
                            RobotData = RobotMove(20,0)
                            '''
                            print (Fore.BLUE + "Sonar in MoveToTarget - " + str(RobotData[5]))
                            print "LeftIR -", RobotData[0]
                            print "CentreIR -", RobotData[1]
                            print "RightIR -", RobotData[2]
                            '''
                        else:
                            attarget = True
            
                    #RobotData = RobotMove(ROBOTRIGHT, 200/TurnRatio, AutoSpeed, 0, 255)
                    #RobotData = RobotMove(ROBOTREVERSE, 30, AutoSpeed, 5, 80)
                    return 1
                else:
                    if TargetData[4] == "LEFT":
                        '''
                        RobotData = RobotMove(ROBOTRIGHT, 10, AutoSpeed, 0, 255)
                        RobotData = RobotMove(ROBOTFORWARD, 30, AutoSpeed, 20, 100)
                        RobotData = RobotMove(ROBOTLEFT, 10, AutoSpeed, 0, 255)
                        '''
                        Result = AlignToTarget(Symbol)
                    else:
                        '''
                        RobotData = RobotMove(ROBOTLEFT, 10, AutoSpeed, 0, 255)
                        RobotData = RobotMove(ROBOTFORWARD, 30, AutoSpeed, 20, 100)
                        RobotData = RobotMove(ROBOTRIGHT, 10, AutoSpeed, 0, 255)
                        '''
                        Result = AlignToTarget(Symbol)
                    
            else:
                print "Target further than 100cm"
                Result = AlignToTarget(Symbol)
                if Result ==1:
                    print "Moving Forward"
                    #RobotData = RobotMove(ROBOTFORWARD, 100, AutoSpeed, 10, 100) #
                    if RobotData[6] < 100 and RobotData[7] < 100:
                        print "Obstacle encountered"
                        return -1


def CheckForTarget(symbol,tries):
    for x in range (0,tries):
        TargetData = SWEARCOpenCV.FindSymbol(BrownObjects)
        if TargetData != -1:#Target present          
            if TargetData[3] == 1: #if its the correct target type
                return TargetData #return straight away if correct symbol found
    return -1


def ScanForTarget(symbol):
    returndata = -1
    print "Scanning for Target"
    TargetData = CheckForTarget(symbol,1)
    #Capture image and check for symbol
    if TargetData == -1:
        print " Not good -No Image in Vicinity"
    else:
        print "I found my Crush"
        Aligned = AlignToTarget(symbol)
        if Aligned == 1:
            return 1
    #Nothing found - Dump the stuff.   
    return returndata




print "Mission Robot Navigation abut to Start"
Run = True

while True:
    
    while Run is True:
        TargetAquired = False
        for x in range (0,4):
            Result = ScanForTarget("VM")
            if Result == -1:
                print "No Target found from scan"
                #turn 120 degrees to the left
                RobotData = RobotMove(0,90)  # Distnace, Angle no sonar or IR threshold so move always completes
            else:
                print "Target Aquired"
                TargetAquired = True
                break
        
        if TargetAquired is True:
            result = MoveToTarget("VM")
            if result == 1:
                Run = False
                print "Mission Accomplished"
            else:
                print "Lost Myself - Need something else"
                #Move to a different location and scan again here
                Run = True
                print "Press button 0 to start"


