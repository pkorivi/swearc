from pyimagesearch.transform import four_point_transform
import imutils
import numpy as np
import cv2

print cv2.__version__
while True:
	capture = cv2.VideoCapture(1)
	#'''
	capture.set(3,640)
	capture.set(4,480)
	ret,img = capture.read()
	#'''
	#img = cv2.imread('f1.jpg',1)
	orig = img.copy()
	#img = cv2.imread('check.png',1)
	imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
	imgHSV = cv2.GaussianBlur(imgHSV,(5,5),0)
	#print imgHSV
	#'''
	#Create bounds for Vending Machine Color
	lower = (0,25,100) #np arrays for upper and lower thresholds
	upper = (33,85,255)
	imgthreshed = cv2.inRange(imgHSV, lower, upper) #threshold imgHSV
	cv2.imshow("HSV_Thresholded", imgthreshed)
	image_1, cnts, hierarchy = cv2.findContours(imgthreshed.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	cv2.drawContours(img,cnts,-1,(0,255,0),2)
	cv2.imshow("Contoured image", img)
	#'''

	for x in range (len(cnts)):
		contourarea = cv2.contourArea(cnts[x]) #get area of contour
		if contourarea > 200: #Discard contours with a small area as this may just be noise
			approxcontour = cv2.approxPolyDP(cnts[x], 0.01 * cv2.arcLength(cnts[x], True), True)
			if len(approxcontour) == 4:
				if hierarchy[0][x][2] != -1:
					'''
					rect = cv2.minAreaRect(cnts[x])
					box = cv2.BoxPoints(rect)
					box = np.int0(box)
					boxcentrex = int(rect[0][0])
					boxcentrey = int(rect[0][1])
					'''
					#correct perspective of found target and output to image named warp   
					warped = four_point_transform(orig, approxcontour.reshape(4, 2))
					cv2.imshow("vending machine", warped)
					new_vm = warped.copy()
					gray1 = cv2.cvtColor(new_vm, cv2.COLOR_BGR2GRAY)
					circles = cv2.HoughCircles(gray1.copy(), cv2.HOUGH_GRADIENT, 1.2, 100,param1=50,param2=70,minRadius=1,maxRadius=200)
					# ensure at least some circles were found
					if circles is not None:
						# convert the (x, y) coordinates and radius of the circles to integers
						circles = np.round(circles[0, :]).astype("int")
					 
						# loop over the (x, y) coordinates and radius of the circles
						for (x, y, r) in circles:
							# draw the circle in the output image, then draw a rectangle
							# corresponding to the center of the circle
							cv2.circle(new_vm, (x, y), r, (0, 255, 0), 4)
							cv2.rectangle(new_vm, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
					 
						# show the output image
						cv2.imshow("output",  new_vm)
						#cv2.waitKey(0)
					else:
						print 'Circles are Doomed'
	cv2.waitKey(3000)				
	cv2.destroyAllWindows()