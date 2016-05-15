void setup() {
  Serial.begin(9600);

}

void loop() {
  performServoControl();
  performSonarControl();
  readSerialCmd();
  delay(100);
}
