int servoArm = 22;
int servoHead = 21;
int servoCamera = 22;

void performServoControl()
{
  // Place holder
}

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

