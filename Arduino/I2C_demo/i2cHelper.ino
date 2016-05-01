void i2cSendSignedInt(signed int SlaveAdd , signed int value, unsigned char command)
{
    Wire.beginTransmission(SlaveAdd); 
    Wire.write(command);
    Wire.write(value & 0xFF);
    Wire.write(value >> 8);
    Wire.endTransmission();
}

void i2cSendSignedLong(signed int SlaveAdd, signed int value, unsigned char command)
{
    Wire.beginTransmission(SlaveAdd); 
    Wire.write(command);
    Wire.write(value & 0xFF);
    Wire.write(value >> 8);
    Wire.write(0);
    Wire.write(0);
    Wire.endTransmission();
}

void i2cReadSignedInt(signed int SlaveAdd, unsigned char command)
{
    Wire.beginTransmission(SlaveAdd);       
    Wire.write(command);
    Wire.endTransmission();
    
    Wire.requestFrom(SlaveAdd,2);          
    
    while (Wire.available())
    {
      z = Wire.read();
      z += Wire.read()*256;               
    }
}
