import cv2
import neatoCom as robot
import sonar
import sys
import RPi.GPIO as GPIO
import serial
import time
from collections import Counter
import math

GPIO.setmode(GPIO.BCM)
GPIO_Interrupt = 21
GPIO_sonar2 = 26
#Configured as pullup, Input
GPIO.setup(GPIO_Interrupt,GPIO.IN, pull_up_down = GPIO.PUD_UP)

def interrupt_callback(channel1):
    RobotMove(-30,0) #MOve back
    RobotMove(0,2)#MOve right by 2 degree
    print 'Check what to do if we are about to hit in right side into the chairs'

GPIO.add_event_detect(GPIO_Interrupt, GPIO.FALLING, callback = interrupt_callback,\
                      bouncetime = 300)


def measure2():
    GPIO.setup(GPIO_sonar2,GPIO.OUT)  # Trigger
    # This function measures a distance
    GPIO.output(GPIO_sonar2, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_sonar2, False)
    GPIO.setup(GPIO_sonar2,GPIO.IN)      # Echo
    start = time.time()
    while GPIO.input(GPIO_sonar2)==0:
        start = time.time()

    while GPIO.input(GPIO_sonar2)==1:
        stop = time.time()
    elapsed = stop-start
    distance = (elapsed * 34300)/2
    return distance

def measure_mode2():
    # This function takes 3 measurements and
    # returns the average.
    distance1=math.floor(measure2())
    time.sleep(0.01)
    distance2=math.floor(measure2())
    time.sleep(0.01)
    distance3=math.floor(measure2())
    time.sleep(0.01)
    distance4=math.floor(measure2())
    time.sleep(0.01)
    distance5=math.floor(measure2())
    data = Counter( [distance1,distance2,distance3,distance4,distance5] )
    #print data.most_common() #prints all unique items and its count
    distance = data.most_common(1) #returns most frequent item
    if distance[0][0] < 600:
        return distance[0][0]
    else:
        return 0


def Close_connection():
    GPIO.cleanup()
    robot.closeSerial()
    sys.exit('Empty Sear Found - Task finished')


def RobotMove(distance, angle):
    #Implement code to move robot in desired way
    robot.iterativeTravel(angle,distance)
    return 1
        

seat_counter = 0

while True:    
    sonar_value_1 = sonar.measure_mode()
    sonar_value_2 = measure_mode2()
    print 'sonar_1_lower',sonar_value_1
    print 'sonar_2_upper',sonar_value_2
    if sonar_value_1<15 and sonar_value_2>20:
        seat_counter += 1
        if seat_counter >= 3:
            print 'Empty Seat'
            #Glow LED for the seat / Display on Screen.
            time.sleep(10)python 
            #Close_connection()
            
    else:
        seat_counter = 0
        print 'seat_counter', seat_counter
    RobotMove(50,0)
