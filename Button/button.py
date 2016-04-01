import numpy as np 
import argparse
import cv2



def button_detect(image):
    boundaries = [([17,15,100],[50,56,200])]

    for (lower,upper) in boundaries:
        lower = np.array(lower,dtype="uint8")
        upper = np.array(upper,dtype="uint8")

        mask = cv2.inRange(image,lower,upper)
        output = cv2.bitwise_and(image,image,mask=mask)

        cv2.imshow("images",np.hstack([image,output]))
        cv2.waitKey(0)

img = cv2.imread('qro.jpg',1)
button_detect(img)
print 'Button Detceted'