import cv2
import numpy as np
from pyimagesearch.transform import four_point_transform
import time
import math
import neatoCom as robot
import sonar
import sys
import RPi.GPIO as GPIO
import serial
import L_scannerpy
import pprint,os

robotstate = ['start','SearchingHuman','NoHuman', 'Req_Destination','Search_Destination',\
              'No_Destination', 'Drive_to_Destination','Task_Finished']
list(enumerate(robotstate))

robotstate = 'start'
#robotstate = 'Search_Destination'
destination_received = False #In interrupt'
destination = 'P'

Letter_frame = [21,61,96,176,170,170]


t_sleep_0_5 = 0.5
t_sleep_1_0 = 1.0
t_sleep_1_5 = 1.5
t_sleep_2_0 = 2.0
t_sleep_3_0 = 3.0
t_sleep_4_0 = 4.0
t_sleep_9_0 = 9.0


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
    global destination_received
    global destination
    destination_received = True #In interrupt'
    destination = 'N'


def interrupt_E(channel1):
    global destination_received
    global destination
    destination_received = True #In interrupt'
    destination = 'E'


def interrupt_W(channel1):
    global destination_received
    global destination
    destination_received = True #In interrupt'
    destination = 'W'


def interrupt_S(channel1):
    global destination_received
    global destination
    destination_received = True #In interrupt'
    destination = 'S'

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

def LookforHuman():
    print 'Change Sonar'
    dist = []
    RobotMove(0,60)
    for i in range(13):
        dist.append(GetData())
        RobotMove(0,-10)
        
    RobotMove(0,70)
    print 'dist', dist
    value = dist.index(min(dist))
    #value_max = dist.index(min(dist))
    print 'value', value
    if dist[value] < 100:
        return 1
    elif dist[value] < 320:
        AligntoHuman(value)
        return -1
    else:
        return -1

def AligntoHuman(position):
    print 'Aligning to Human'
    RobotMove(0,(6-position)*10)

def RobotMove(distance, angle):
    sleep = t_sleep_2_0
    if (distance != 0):
        if(distance<250):
            sleep = t_sleep_2_0
        elif (distance<600):
            sleep = t_sleep_3_0+t_sleep_1_0
        else:
            sleep = t_sleep_9_0

    if (angle != 0):
        if(angle<5):
            sleep = t_sleep_0_5
        elif (angle<20):
            sleep = t_sleep_1_0
        elif (angle<61):
            sleep = t_sleep_1_5
        else:
            sleep = t_sleep_2_0+t_sleep_0_5

    robot.iterativeTravel(angle,distance,sleep)
    return 1

def MoveToTarget(GivenLetter):
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
            
            #if letter in Target Data == input direction then RobotMove.
            if TargetData[6] == GivenLetter: #or 'E', 'S', 'N'
                RobotData = RobotMove(200,0)
            # then stop... 
                    


#########Need to be chnaged to a switch
Run = True
print "Mission: Robot Navigation about to Start"
command = "espeak -ven+m1 -a 200 -p 30 -s 150 -g 12 'Hello I am Moose, Its time for Task 2' 2>/dev/null > /dev/null"
os.system(command)
last = 0
time.sleep(3)
command = "espeak -ven+m1 -a 200 -p 30 -s 150 -g 12 'Please Press the Start Button ' 2>/dev/null > /dev/null"
os.system(command)
last = 0


while True:
    while Run is True:
        #time.sleep(1)
        print "Loop"
        for case in switch(robotstate):
			if case('start'):
				print 'Start - caliberate'
				robotstate = 'SearchingHuman'
				command = "espeak -ven+m1 -a 200 -p 30 -s 150 -g 12 'Human, dear Human. Where are you' 2>/dev/null > /dev/null"
                                os.system(command)
                                last = 0
                                time.sleep(4)
				break
			if case('SearchingHuman'):
				print 'Searching Human'
				result = LookforHuman()
				if result != -1:
                                    AligntoHuman(result)
                                    robotstate = 'Req_Destination'
                                else :
                                    robotstate = 'NoHuman'
				break #break for searchingtarget
			if case('NoHuman'):
				print 'No Human'
				RobotData = RobotMove(600,0)
				robotstate = 'SearchingHuman'
				break
			if case('Req_Destination'):
				print 'Request Destination'
				command = "espeak -ven+m1 -a 200 -p 30 -s 150 -g 12 'Press one of N, E, W, S direction on the Keyboard ' 2>/dev/null > /dev/null"
                                os.system(command)
                                last = 0
                                time.sleep(4)
                                while destination_received == False:
                                    pass
                                
                                command = "espeak -ven+m1 -a 200 -p 30 -s 150 -g 12 'Thank You, let me go to the specified destinaton' 2>/dev/null > /dev/null"
                                os.system(command)
                                last = 0
                                time.sleep(4)
                                
                                print destination
                                #speak destination
                                if destination != 'P':
                                    robotstate = 'Search_Destination'
                                else:
                                    robotstate = 'No_Destination'
				break
                        if case('No_Destination'):
				print 'No Destination'
				destination_received = False
				robotstate = 'Req_Destination'
				break
			if case('Search_Destination'):
                                result = L_scannerpy.FindLetter(destination,Letter_frame)
                                if result != -1:
                                    robotstate = 'Drive_to_Destination'
                                else:
                                    RobotMove(0,15)
                                    print 'Move and try for destination again'
				break
			if case('Drive_to_Destination'):
				print 'Drive to Destination'
				RobotData = RobotMove(2000,0)
				robotstate = 'Task_Finished'
				break
			if case('Task_Finished'):
				print 'Task Fnished'
				command = "espeak -ven+m1 -a 200 -p 30 -s 150 -g 12 'I Reached Destination. Bye Bye Have a good time' 2>/dev/null > /dev/null"
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
