/* Ping))) Sensor

   This sketch reads a PING))) ultrasonic rangefinder and returns the
   distance to the closest object in range. To do this, it sends a pulse
   to the sensor to initiate a reading, then listens for a pulse
   to return.  The length of the returning pulse is proportional to
   the distance of the object from the sensor.

   The circuit:
    * +V connection of the PING))) attached to +5V
    * GND connection of the PING))) attached to ground
    * SIG connection of the PING))) attached to digital pin 7

   http://www.arduino.cc/en/Tutorial/Ping

 */

// this constant won't change.  It's the pin number
// of the sensors output:
const int pingPinSonar1_trig = 9;
const int pingPinSonar1_echo = 8;

const int pingPinSonar2_trig = 7;
const int pingPinSonar2_echo = 6;

const int pingPinSonar3_trig = 5;
const int pingPinSonar3_echo = 4;

const int pingPinSonar4_trig = 3;
const int pingPinSonar4_echo = 2;

unsigned int sonarData[4] = {21, 'A', 'B', 'C'};

void ReadSonarSensor1()
{
  // establish variables for duration of the ping,
  // and the distance result in inches and centimeters:
  long duration, inches, cm;

  // The PING))) is triggered by a HIGH pulse of 2 or more microseconds.
  // Give a short LOW pulse beforehand to ensure a clean HIGH pulse:
  pinMode(pingPinSonar1_trig, OUTPUT);
  digitalWrite(pingPinSonar1_trig, LOW);
  delayMicroseconds(2);
  digitalWrite(pingPinSonar1_trig, HIGH);
  delayMicroseconds(5);
  digitalWrite(pingPinSonar1_trig, LOW);

  // The same pin is used to read the signal from the PING))): a HIGH
  // pulse whose duration is the time (in microseconds) from the sending
  // of the ping to the reception of its echo off of an object.
  pinMode(pingPinSonar1_echo, INPUT);
  duration = pulseIn(pingPinSonar1_echo, HIGH);

  // convert the time into a distance
  //inches = microsecondsToInches(duration);
  cm = microsecondsToCentimeters(duration);

  if( 255 <= cm )
  {
    sonarData[0] = 255;
  }
  else
  {
    sonarData[0] = cm;
  }
  
}

void ReadSonarSensor2()
{
  // establish variables for duration of the ping,
  // and the distance result in inches and centimeters:
  long duration, inches, cm;

  // The PING))) is triggered by a HIGH pulse of 2 or more microseconds. trig - 7(o/p); echo - 6(i/p)
  // Give a short LOW pulse beforehand to ensure a clean HIGH pulse:
  pinMode(pingPinSonar2_trig, OUTPUT);
  digitalWrite(pingPinSonar2_trig, LOW);
  delayMicroseconds(2);
  digitalWrite(pingPinSonar2_trig, HIGH);
  delayMicroseconds(5);
  digitalWrite(pingPinSonar2_trig, LOW);

  // The same pin is used to read the signal from the PING))): a HIGH
  // pulse whose duration is the time (in microseconds) from the sending
  // of the ping to the reception of its echo off of an object.
  pinMode(pingPinSonar2_echo, INPUT);
  duration = pulseIn(pingPinSonar2_echo, HIGH);

  // convert the time into a distance
  //inches = microsecondsToInches(duration);
  cm = microsecondsToCentimeters(duration);

  if( 255 <= cm )
  {
    sonarData[1] = 255;
  }
  else
  {
    sonarData[1] = cm;
  }
}

void ReadSonarSensor3()
{
  // establish variables for duration of the ping,
  // and the distance result in inches and centimeters:
  long duration, inches, cm;

  // The PING))) is triggered by a HIGH pulse of 2 or more microseconds. trig - 7(o/p); echo - 6(i/p)
  // Give a short LOW pulse beforehand to ensure a clean HIGH pulse:
  pinMode(pingPinSonar3_trig, OUTPUT);
  digitalWrite(pingPinSonar3_trig, LOW);
  delayMicroseconds(2);
  digitalWrite(pingPinSonar3_trig, HIGH);
  delayMicroseconds(5);
  digitalWrite(pingPinSonar3_trig, LOW);

  // The same pin is used to read the signal from the PING))): a HIGH
  // pulse whose duration is the time (in microseconds) from the sending
  // of the ping to the reception of its echo off of an object.
  pinMode(pingPinSonar3_echo, INPUT);
  duration = pulseIn(pingPinSonar3_echo, HIGH);

  // convert the time into a distance
  //inches = microsecondsToInches(duration);
  cm = microsecondsToCentimeters(duration);

  if( 255 <= cm )
  {
    sonarData[2] = 255;
  }
  else
  {
    sonarData[2] = cm;
  }
}

void ReadSonarSensor4()
{
  // establish variables for duration of the ping,
  // and the distance result in inches and centimeters:
  long duration, inches, cm;

  // The PING))) is triggered by a HIGH pulse of 2 or more microseconds. trig - 7(o/p); echo - 6(i/p)
  // Give a short LOW pulse beforehand to ensure a clean HIGH pulse:
  pinMode(pingPinSonar4_trig, OUTPUT);
  digitalWrite(pingPinSonar4_trig, LOW);
  delayMicroseconds(2);
  digitalWrite(pingPinSonar4_trig, HIGH);
  delayMicroseconds(5);
  digitalWrite(pingPinSonar4_trig, LOW);

  // The same pin is used to read the signal from the PING))): a HIGH
  // pulse whose duration is the time (in microseconds) from the sending
  // of the ping to the reception of its echo off of an object.
  pinMode(pingPinSonar4_echo, INPUT);
  duration = pulseIn(pingPinSonar4_echo, HIGH);

  // convert the time into a distance
  //inches = microsecondsToInches(duration);
  cm = microsecondsToCentimeters(duration);

  if( 255 <= cm )
  {
    sonarData[3] = 255;
  }
  else
  {
    sonarData[3] = cm;
  }
}

void performSonarControl() {
    
  ReadSonarSensor1();
  ReadSonarSensor2();
  ReadSonarSensor3();
  ReadSonarSensor4();
  /*Serial.print(inches);
  Serial.print("in, ");
  Serial.print(cm);
  Serial.print("cm");
  Serial.println();

  delay(100);*/
}

long microsecondsToInches(long microseconds) {
  // According to Parallax's datasheet for the PING))), there are
  // 73.746 microseconds per inch (i.e. sound travels at 1130 feet per
  // second).  This gives the distance travelled by the ping, outbound
  // and return, so we divide by 2 to get the distance of the obstacle.
  // See: http://www.parallax.com/dl/docs/prod/acc/28015-PING-v1.3.pdf
  return microseconds / 74 / 2;
}

long microsecondsToCentimeters(long microseconds) {
  // The speed of sound is 340 m/s or 29 microseconds per centimeter.
  // The ping travels out and back, so to find the distance of the
  // object we take half of the distance travelled.
  return microseconds / 29 / 2;
}

void getSonarData(int* outData)
{
  outData[0] = sonarData[0];
  outData[1] = sonarData[1];
  outData[2] = sonarData[2];
  outData[3] = sonarData[3];  
}
