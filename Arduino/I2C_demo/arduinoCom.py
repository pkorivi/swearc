import serial

class Arduino:

  def __init__(self):
    print("Arduino object created")

  def startCom(self):
    try:
      self.ser = serial.Serial('/dev/ttyAMA0',baudrate=9600,timeout=0)
    except:
      print("Arduino device not available!")

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
      return self.ser.read(10000)
    except:
      print("sendGenericGetCommand: Failed to write to arduino")

  def setMotorCount(self,value):
    try:
      self.ser.write('set.motorcount '+value+'\n')
    except:
      print("setMotorCount: Failed to write to arduino")
    

