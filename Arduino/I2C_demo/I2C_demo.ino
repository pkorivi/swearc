 #include <Wire.h>

 #define Motor_1 0x05
 #define Motor_2 0x0A

signed int z;
signed int motor_counts = 1800;

void setup() 
{
  Wire.begin();
  Serial.begin(9600);
}

void loop() 
{
  i2cSendSignedInt(Motor_1,20, 0);		//set the maxspeed (0) to 255 
  delay(100);					                //give a 100ms delay to process the command
  i2cSendSignedInt(Motor_2,20, 0);			
  delay(100);
        
        
  i2cSendSignedLong(Motor_1,0, 3);			//set the encoder counter (3) to 0
  delay(100);						//give a 100ms delay to process the command        
  i2cSendSignedLong(Motor_2,0, 3);			
  delay(100);		
        
  Serial.println("Motor_1");                              // Serial print Motor_1
  i2cSendSignedLong(Motor_1,motor_counts, 8);			//set the absolute go to posuition (4) to 1800 counts
  //i2cReadSignedInt(Motor_1,3);                            // Read the Encoder Position.
  
  Serial.println("Motor_2");                              // Serial print Motor_1
  i2cSendSignedLong(Motor_2,motor_counts, 8);      //set the absolute go to posuition (4) to 1800 counts
  //i2cReadSignedInt(Motor_2,3);
    
   /* while(z <= 1800)                                        // wait till Motor_1 reaches its position
     {
         delay(100);
         i2cReadSignedInt(Motor_1,3);
         Serial.println(z);
     }
     
     Serial.println("Motor_2");
     i2cSendSignedLong(Motor_2,1800, 4);			// set the absolute go to posuition (4) to 1800 counts
     i2cReadSignedInt(Motor_2,3);                          
     
    while(z <= 1800)                                        // Wait till Motor_2 reaches its position
     {
         delay(100);
         i2cReadSignedInt(Motor_2,3);
         Serial.println(z);
     }   
     
    i2cSendSignedInt(Motor_1,255, 0);	                 // set the motor speed to Maximum 
    i2cSendSignedInt(Motor_2,255, 0);	
    i2cSendSignedLong(Motor_1,900, 4);                    
    i2cSendSignedLong(Motor_2,900, 4);		*/				

    readSerialCmd();
    
   delay(5000);																								
} 






