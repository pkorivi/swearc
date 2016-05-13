from sys import argv
import zbar
from PIL import Image
import cv2
import json

# create a reader
def QRDetect(image):
    scanner = zbar.ImageScanner()

    # configure the reader
    scanner.parse_config('enable')
    # obtain image data
    #gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY,dstCn=0)
    pil = Image.fromarray(image)
    width, height = pil.size
    raw = pil.tobytes()
    # wrap image data
    image = zbar.Image(width, height, 'Y800', raw)
    # scan the image for barcodes
    scanner.scan(image)

    # extract results
    for symbol in image:
        # do something useful with results
        if symbol.data == "None":
            print "Data Not read"
            return "error"
        else:
            print symbol.data
            parsed_json = json.loads(symbol.data)
            return parsed_json
            #return symbol.data


#Reag Image and call QR Code Detection Function
#im = cv2.imread('oo.jpg',0)
picamera = 0
qrcamera = cv2.VideoCapture(picamera)
ret, im = qrcamera.read()
#Release camera
qrcamera.release()
imG = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
cv2.imshow('QR_Code',imG)
cv2.waitKey(2000)
jsondata = QRDetect(imG)
print jsondata
'''
b = jsondata[' id ']
train = jsondata[' t r a i n ']
car = jsondata[' car ']
seat = jsondata[' s e a t ']
platform = jsondata[' platform']
time = jsondata[' time ']
#print(parsed_json[' id '])
print b,train,car,seat,platform,time
#print type(b)
'''
print 'QR Code done'
            
 
