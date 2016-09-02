#include <compat/deprecated.h>
#include <Servo.h>

#define FLOOR_THRESHOLD   70

extern unsigned int sonarData[4];

Servo myservo;  // create servo object to control a servo
// twelve servo objects can be created on most boards

void setup() {
  Serial.begin(9600);
  sbi(DDRB, 5);   //set as o/p pin(pin 13 of arduino uno) for generating interrupt for rasberryPi
  cbi(PORTB, 5);  //generates logic 0 at pin13 of arduino uno

  sbi(DDRC, 4); //set as o/p pin for LED
  cbi(PORTC, 4);

  myservo.attach(10);  // attaches the servo on pin 9 to the servo object
}

void EdgeDetection()
{
  ReadSonarSensor1();

  if( FLOOR_THRESHOLD <= sonarData[0] )
  {
    sbi(PORTB, 5);  //generates logic 1 at pin13 of arduino uno
    delay(10);
    cbi(PORTB, 5);  //generates logic 0 at pin13 of arduino uno

    //Serial.write('A');
  }
}

void loop() {
  //performServoControl();
  performServoControl();
  EdgeDetection();
  performSonarControl();
  readSerialCmd();
  delay(50);
}
