import cv2
import numpy as np
import time
import math
import neatoCom as robot


def RobotMove(distance, angle):
    #Implement code to move robot in desired way
    robot.iterativeTravel(angle,distance)
    return 1

RobotData = RobotMove(0,60)
RobotData = RobotMove(100,0)
RobotData = RobotMove(0,-60)

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
