import imutils
import numpy as np
import cv2

#print help(cv2.xfeatures2d)

detector = cv2.xfeatures2d.SURF_create(1000)
HomeSymbol = cv2.imread("s.jpg")
HomeSymbolKeypoints, HomeSymbolDescriptors = detector.detectAndCompute(HomeSymbol , None)

print 'HomeSymbolKeypoints', HomeSymbolKeypoints

print 'HomeSymbolDescriptors', HomeSymbolDescriptors