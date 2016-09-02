import serial
import arduinoCom

arduino = arduinoCom.Arduino()
for i in range (10):
    print 'i',i
    if arduino.connect() == 1:
        print 'connection established'
        break
    else:
        print 'Connection failed'

print arduino.getSonar()

