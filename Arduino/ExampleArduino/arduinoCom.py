import serial
import array

class Arduino:

  def __init__(self):
    print("Arduino object created")

  def startCom(self, device):
    try:
      self.ser = serial.Serial(device ,9600, timeout=6)
      return 1
    except:
      print("Arduino device not available!")
      return 0

  def closeCom(self):
    try:
      self.ser.close()
      print("serial port closed")
    except:
      print("setMotorCount: Failed to write to arduino")

  def sendGenericSetCommand(self,command,value):
    try:
      self.ser.write('set.'+command+' '+value+'\n')
    except:
      print("sendGenericSetCommand: Failed to write to arduino")

  def sendGenericGetCommand(self,command,value):
    try:
      self.ser.flushInput()
      self.ser.write('get.'+command+' '+value+'\n')
      return self.ser.readline()
    except:
      print("sendGenericGetCommand: Failed to write to arduino")
      return 0

  def setServos(self,servo1, servo2, servo3):
    try:
      self.ser.write("set.servos "+str(servo1)+","+str(servo2)+","+str(servo3)+"\n")
      return 1
    except:
      print("setServos: Failed to write to arduino")
      return 0

  def setArm(self,servo1):
    try:
      self.ser.flushInput()
      self.ser.write("set.servos "+str(servo1)+",0,0\n")
      tmpArray = array.array('B', self.ser.readline().rstrip())
      if tmpArray[0] == int(servo1):
        return 1
      else:
        return 0
    except:
      print("setServos: Failed to write to arduino")
      return 0

  def setServo(self,servo, value):
    try:
      self.ser.write("set.servo: "+servo+" "+str(value)+"\n")
      return 1
    except:
      print("setServos: Failed to write to arduino")
      return 0

  def getSonar(self):
    try:
      self.ser.flushInput()
      self.ser.write("get.sonar\n")
      tmpArray = array.array('B', self.ser.readline().rstrip())
      return tmpArray
    except:
      print("getSonar: Faild to write and read from arduino")
      return 0

  def sayHello(self):
    try:
      self.ser.flushInput()
      self.ser.write("Hi.Arduino\n")
      if self.ser.readline().rstrip() == 'Hi.Raspberry':
        return 1
      else:
        self.closeCom()
        return 0
    except:
      print("sayHello: Failed to write and read from arduino")
      return 0

  def connect(self):
    connectedToArduino = 0
    if self.startCom('/dev/ttyACM0') == 1 and self.sayHello() == 1:
      print("Connected to Arduino")
      return 1
    elif self.startCom('/dev/ttyACM1') == 1 and self.sayHello() == 1:
      print("Connected to Arduino")
      return 1
    elif self.startCom('/dev/ttyACM2') == 1 and self.sayHello() == 1:
      print("Connected to Arduino")
      return 1
    elif self.startCom('/dev/ttyACM3') == 1 and self.sayHello() == 1:
      print("Connected to Arduino")
      return 1
    else:
      print("Couldn't connect to Arduino!!!")
      return 0
      
  
  
    

