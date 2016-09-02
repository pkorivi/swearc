import cv2
import neatoCom as robot
import sys
import RPi.GPIO as GPIO
import serial
import time
from collections import Counter
import math
import arduinoCom
import pprint,os

Run = False

seat_counter = 0

Seat_Thresh = 10
Edge_Thresh = 15
Forward_Thresh = 10

GPIO.setmode(GPIO.BCM)
GPIO_Interrupt = 26
GPIO_Start = 23
GPIO_Emergency = 24

#Configured as pullup, Input
GPIO.setup(GPIO_Interrupt,GPIO.IN, pull_up_down = GPIO.PUD_UP)
#Configured as pullup, Input
GPIO.setup(GPIO_Start,GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(GPIO_Emergency,GPIO.IN, pull_up_down = GPIO.PUD_UP)

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


def interrupt_callback(channel1):
    sonar = arduino.getSonar()
    RobotMove(-30,0) #MOve back
    if sonar[0] < Seat_Thresh:  #Hitting the seats
        RobotMove(0,-2)#MOve right by 2 degree
    elif sonar[2] < Forward_Thresh: #Hitting Forward
        Close_connection()
    elif sonar[3] > Edge_Thresh: #Faling of Edge
        RobotMove(0,2)#MOve right by 2 degree
    else:
        pass


#Interrupt Events
GPIO.add_event_detect(GPIO_Start, GPIO.FALLING, callback = interrupt_start,\
                      bouncetime = 2000)
GPIO.add_event_detect(GPIO_Emergency, GPIO.FALLING, callback = interrupt_emergency,\
                      bouncetime = 2000)
GPIO.add_event_detect(GPIO_Interrupt, GPIO.RISING, callback = interrupt_callback,\
                      bouncetime = 2000)



def RobotMove(distance, angle):
    sleep = t_sleep_2_0
    if (distance != 0):
        if(distance<250):
            sleep = 2.5
        elif (distance<500):
            sleep = 4
        else:
            sleep = 10

    if (angle != 0):
        if(angle<5):
            sleep = 1.5
        elif (angle<25):
            sleep = 2.5
        elif (angle<61):
            sleep = 4
        else:
            sleep = 6

    robot.iterativeTravel(angle,distance,sleep)
    return 1

def Close_connection():
    GPIO.cleanup()
    robot.closeSerial()
    sys.exit('Empty Sear Found - Task finished')


arduino = arduinoCom.Arduino()
for i in range (10):
    print 'i',i
    if arduino.connect() == 1:
        print 'connection established'
        break
    else:
        print 'Connection failed'


command = "espeak -ven+m1 -a 200 -p 30 -s 150 -g 12 'Helo, Nice to Meet You' 2>/dev/null > /dev/null"
os.system(command)
time.sleep(4)

command = "espeak -ven+m1 -a 200 -p 30 -s 150 -g 12 'Please Wait, till I find an empty seat for you' 2>/dev/null > /dev/null"
os.system(command)
time.sleep(4)

while True:
    seat_counter = 0
    while Run is True: #Waiting for Button to be pressed
        sonar = arduino.getSonar()
        sonar_value_1 = sonar[0]
        sonar_value_2 = sonar[1]
        print 'sonar_1_lower',sonar_value_1
        print 'sonar_2_upper',sonar_value_2
        if sonar_value_1<15 and sonar_value_2>20:
            seat_counter += 1
            if seat_counter >= 3:
                print 'Empty Seat'
                command = "espeak -ven+m1 -a 200 -p 30 -s 150 -g 12 'Yipee, This is Your Empty Seat, Bye See You soon' 2>/dev/null > /dev/null"
                os.system(command)
                time.sleep(6)
                time.sleep(10) 
                Close_connection()
        else:
            seat_counter = 0
            print 'seat_counter', seat_counter
        RobotMove(50,0)
