void readSerialCmd()
{
  String inCmd = "";
  String inValue = "";
  String inSubCmd = "";
  bool subCmdPresent = false;
  short int valueCount = 0;
  int values[5];
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
    else if( inChar == ':' )
    {
      subCmdPresent = true;
    }
    else if( inChar == ',' )
    {
      if (inValue != "")
      {
        values[valueCount] = inValue.toInt();
      }
      inValue = "";
      valueCount++;
    }
    else if(isAscii(inChar))
    {
      if(subCmdPresent)
      {
        inSubCmd += (char)inChar;
      }
      else
      {
        inCmd += (char)inChar; 
      }
    }

    if (inChar == '\n')
    {
      if (inValue != "")
      {
        values[valueCount] = inValue.toInt();
      }
      interpretSerialCmd(inCmd,inSubCmd,&values[0]);
    }
  }
}

void interpretSerialCmd(String cmd,String subCmd, int* values)
{

  if ( (String)"Hi.Arduino" == cmd )
  {
    Serial.println("Hi.Raspberry"); 
    sbi(PORTC, 4); 
  }
  else if ((String)"get.sonar" == cmd)
  {
    int sonarData[4];
    getSonarData(&sonarData[0]);
    Serial.write(sonarData[0]);
    Serial.write(sonarData[1]);
    Serial.write(sonarData[2]);
    Serial.write(sonarData[3]);
    Serial.write('\r');
    Serial.write('\n');
  }
  else if ((String)"set.servos" == cmd)
  {
    setServoArm(values[0]);
    setServoHead(values[1]);
    setServoCamera(values[2]);

    Serial.write(getServoArm());
    Serial.write('\r');
    Serial.write('\n');
  }
  else if ((String)"set.servo" == cmd)
  {
    if ((String)"head" == subCmd)
    {
      setServoHead(values[0]);
    }
    else if ((String)"arm" == subCmd)
    {
      setServoArm(values[0]);
    }
    else if ((String)"camera" == subCmd)
    {
      setServoCamera(values[0]);
    }
  }
  else if ((String)"get.servo" == cmd)
  {
    if ((String)"head" == subCmd)
    {
      Serial.write(getServoHead());
    }
    else if ((String)"arm" == subCmd)
    {
      Serial.write(getServoArm());
    }
    else if ((String)"camera" == subCmd)
    {
      Serial.write(getServoCamera());
    }
    Serial.write('\r');
    Serial.write('\n');
  }
  else if ((String)"get.servos" == cmd)
  {
    int tmpValues[3];
    getServos(&tmpValues[0]);

    Serial.write(tmpValues[0]);
    Serial.write(tmpValues[1]);
    Serial.write(tmpValues[2]);
    Serial.write('\r');
    Serial.write('\n');    
  }
  else
  {
    Serial.println("Cmd_Error");
  }  
}
