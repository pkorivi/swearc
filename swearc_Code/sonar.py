import time
import RPi.GPIO as GPIO
from collections import Counter
import math
# -----------------------
# Define some functions
# -----------------------

def measure():
  # This function measures a distance
  GPIO.output(GPIO_TRIGGER, True)
  time.sleep(0.00001)
  GPIO.output(GPIO_TRIGGER, False)
  start = time.time()

  while GPIO.input(GPIO_ECHO)==0:
    start = time.time()

  while GPIO.input(GPIO_ECHO)==1:
    stop = time.time()

  elapsed = stop-start
  distance = (elapsed * 34300)/2

  return distance

def measure_average():
  # This function takes 3 measurements and
  # returns the average.
  distance1=measure()
  time.sleep(0.1)
  distance2=measure()
  time.sleep(0.1)
  distance3=measure()
  distance = distance1 + distance2 + distance3
  distance = distance / 3
  return distance

def measure_mode():
  # This function takes 3 measurements and
  # returns the average.
  distance1=math.floor(measure())
  time.sleep(0.01)
  distance2=math.floor(measure())
  time.sleep(0.01)
  distance3=math.floor(measure())
  time.sleep(0.01)
  distance4=math.floor(measure())
  time.sleep(0.01)
  distance5=math.floor(measure())
  data = Counter( [distance1,distance2,distance3,distance4,distance5] )
  #print data.most_common() #prints all unique items and its count
  distance = data.most_common(1) #returns most frequent item
  return distance[0][0]

# -----------------------
# Main Script
# -----------------------

# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)

# Define GPIO to use on Pi
GPIO_TRIGGER = 23
GPIO_ECHO    = 24

print "Ultrasonic Measurement"

# Set pins as output and input
GPIO.setup(GPIO_TRIGGER,GPIO.OUT)  # Trigger
GPIO.setup(GPIO_ECHO,GPIO.IN)      # Echo

# Set trigger to False (Low)
GPIO.output(GPIO_TRIGGER, False)

# Wrap main content in a try block so we can
# catch the user pressing CTRL-C and run the
# GPIO cleanup function. This will also prevent
# the user seeing lots of unnecessary error
# messages.
#d = measure_mode()
#print d
#print d[0][0]

'''
try:

  while True:

    distance = measure_average()
    print "Distance : %.1f" % distance
    time.sleep(1)

except KeyboardInterrupt:
  # User pressed CTRL-C
  # Reset GPIO settings
  GPIO.cleanup()
'''
