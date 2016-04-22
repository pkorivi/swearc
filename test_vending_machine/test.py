import cv2
import numpy as np 
import sys
from colorama import init,Fore
'''
print cv2.__version__
print (sys.version)
'''
print (Fore.WHITE + "Scanning for target")

img = cv2.imread('f2.jpg',1)
imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
cv2.imshow("imgHSV", imgHSV)
cv2.waitKey(3000)
print imgHSV