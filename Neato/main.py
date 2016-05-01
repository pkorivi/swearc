#import XboxController
import time
import serial
import csv

def getScan():
    ser.timeout = 2
    ser.flushInput()
    ser.write(b'getldsscan\n')
    s = ser.read(10000)
    #print(s)
    rows = s.split("\r")

    distance = []
    angle = []
    intensity = []
    errorcode = []
    done = 0
    for row in rows:
        if "AngleInDegrees" in row:
            print(row)
        elif "getldsscan" in row:
            print(row)
        elif "ROTATION" in row:
            done = 1
            print(row)
        elif done == 0 and row != "":
            #print(row)
            column = row.split(",")
            angle       += [int(column[0])]
            distance    += [int(column[1])]
            intensity   += [int(column[2])]
            errorcode   += [int(column[3])]
    print("Angle:%d deg distance:%d mm" % (angle[0], distance[0]))
    print("Angle:%d deg distance:%d mm" % (angle[90], distance[90]))
    print("Angle:%d deg distance:%d mm" % (angle[180], distance[180]))
    print("Angle:%d deg distance:%d mm" % (angle[270], distance[270]))

    s2 = ""
    for c in s:
        if c == ",":
            c = ";"
        s2 += c
    myfile = open("scan.csv","w")
    myfile.write(s2)

def getBattery():
    ser.timeout = 2
    ser.flushInput()
    ser.write(b'getcharger\n')
    s = ser.read(10000)
    rows = s.split("\r")

    SOC = 0
    Ubat = 0
    for row in rows:
        column = row.split(",")
        if "FuelPercent" in row:
            SOC = int(column[1])
        elif "VBattV" in row:
            Ubat = float(column[1])
    print("SOC:%d/100  %.2fV"%(SOC,Ubat))
    if SOC <= 30 or Ubat < 14.0:
        raise Exception("Please recharge batteries")

def iterativeTravel(angle,distance):
    if angle != 0:
        Lmotor = int(angle*190/90)
        Rmotor = int(-Lmotor)
        speed = 200
        setmotor = "setmotor "+str(Lmotor)+" "+str(Rmotor)+" "+str(speed)
        setmotor = setmotor+"\n"
        print(setmotor)
        ser.write(setmotor.encode())
        time.sleep(2)
    if distance > 0:
        Lmotor = int(distance)
        Rmotor = int(distance)
        speed = 200
        setmotor = "setmotor "+str(Lmotor)+" "+str(Rmotor)+" "+str(speed)
        setmotor = setmotor+"\n"
        print(setmotor)
        ser.write(setmotor.encode())
        time.sleep(4)


dT = 0;
T = time.clock()
print("T=%.3f" % T)
T_old = T;
try:
    ser = serial.Serial('/dev/ttyACM0')
    #time.sleep(5)
##    xboxCont = XboxController.XboxController(
##        controllerCallBack = None,
##        joystickNo = 0,
##        deadzone = 0.1,
##        scale = 1,
##        invertYAxis = True)
##
##    xboxCont.start()

    ser.write(b'testmode on\n')
    time.sleep(0.3)
    ser.write(b'playsound 0\n')
    time.sleep(0.3)
    ser.write(b'setldsrotation on\n')
    time.sleep(4)
    getBattery()
    getScan()

    speed = 0
    diff = 0
    Lmotor = 0
    Rmotor = 0
    lastSpeed = 0
    setmotor = ""

    while 1:
        T_old = T
        T = time.clock()
        dT = T - T_old

        time.sleep(0.1)
##        diff = xboxCont.LTHUMBX*(2000 - 1000*xboxCont.LTHUMBY*xboxCont.LTHUMBY)
##        speed = int(300*max(abs(xboxCont.LTHUMBY),abs(xboxCont.LTHUMBX)))
##        Lmotor = int(xboxCont.LTHUMBY*1000+diff/2)
##        Rmotor = int(xboxCont.LTHUMBY*1000-diff/2)
##        #iterativeTravel(-90,100)
##        #print(speed)
##        if speed == 0:
##            if speed != lastSpeed:
##                #print("setmotor 1 1 10")
##                ser.write(b'setmotor 1 1 10\n')
##        else:
##            setmotor = "setmotor "+str(Lmotor)+" "+str(Rmotor)+" "+str(speed)
##            #print(setmotor)
##            setmotor = setmotor+"\n"
##            ser.write(setmotor.encode())
##        lastSpeed = speed

#Ctrl C
except KeyboardInterrupt:
    print("\nUser cancelled")
    ser.write(b'setldsrotation off\n')
    ser.write(b'playsound 3\n')
    ser.write(b'testmode off\n')
##    xboxCont.stop()
    ser.close()
    print("serial port closed and xbox controller off")
#Other exit
except:
    print("\nOther error")
    ser.write(b'setldsrotation off\n')
    ser.write(b'playsound 3\n')
    ser.write(b'testmode off\n')
##    xboxCont.stop()
    ser.close()
    print("serial port closed and xbox controller off")
    raise

