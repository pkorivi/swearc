/* Sweep
 by BARRAGAN <http://barraganstudio.com>
 This example code is in the public domain.

 modified 8 Nov 2013
 by Scott Fitzgerald
 http://www.arduino.cc/en/Tutorial/Sweep
*/

#include <Servo.h>

int servoArm = 22;
int servoHead = 21;
int servoCamera = 22;

extern Servo myservo;  // create servo object to control a servo
// twelve servo objects can be created on most boards

int pos = 0;    // variable to store the servo position

void performServoControl() 
{
  /*for (pos = 0; pos <= 180; pos += 1) { // goes from 0 degrees to 180 degrees
    // in steps of 1 degree
    myservo.write(pos);              // tell servo to go to position in variable 'pos'
    delay(15);                       // waits 15ms for the servo to reach the position
  }
  for (pos = 180; pos >= 0; pos -= 1) { // goes from 180 degrees to 0 degrees
    myservo.write(pos);              // tell servo to go to position in variable 'pos'
    delay(15);                       // waits 15ms for the servo to reach the position
  }*/

  myservo.write(servoArm);
}

/*void performServoControl()
{
  // Place holder
}*/

void setServoArm(int value)
{
  servoArm = value;
}

void setServoHead(int value)
{
  servoHead = value;
}

void setServoCamera(int value)
{
  servoCamera = value;
}

int getServoArm()
{
  return servoArm;
}

int getServoHead()
{
  return servoHead;
}

int getServoCamera()
{
  return servoCamera;
}

void getServos(int* outValue)
{
  outValue[0] = servoArm;
  outValue[1] = servoHead;
  outValue[2] = servoCamera;
}

