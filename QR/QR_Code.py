from sys import argv
import zbar
import Image
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
    raw = pil.tostring()
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
img = cv2.imread('qr.jpg',0)
jsondata = QRDetect(img)

b = jsondata[' id ']
train = jsondata[' t r a i n ']
car = jsondata[' car ']
seat = jsondata[' s e a t ']
platform = jsondata[' platform']
time = jsondata[' time ']
#print(parsed_json[' id '])
print b,train,car,seat,platform,time
#print type(b)
print 'QR Code done'
            
 
