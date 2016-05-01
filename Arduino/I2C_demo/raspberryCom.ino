void readSerialCmd()
{
  String inCmd = "";
  String inValue = "";
  while(Serial.available() > 0)
  {
    int inChar = Serial.read();
    if (isDigit(inChar))
    {
      inValue += (char)inChar;
    }
    else if(isSpace(inChar) || inChar == '\n')
    {
      // Ignore for now
    }
    else if(isAscii(inChar))
    {
      inCmd += (char)inChar; 
    }

    if (inChar == '\n')
    {
      interpretSerialCmd(inCmd,inValue);
    }
  }
}

void interpretSerialCmd(String cmd, String value)
{
  if ( (String)"set.motorcount" == cmd )
  {
    motor_counts = value.toInt();  
  }
  else if ( (String)"get.motorcount" == cmd )
  {
    Serial.println(String(motor_counts));
  }
  else
  {
    Serial.println("Cmd_Error");
  }  
}
