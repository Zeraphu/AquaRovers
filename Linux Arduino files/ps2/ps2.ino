#include<PS2X_lib.h>
PS2X ps2;

byte type = 0; // 0 = Unknown, 1 = Dual Shock 
byte vibrate = 0; // vibration motor speed
int error = 0; // error recieved during config
int data = 12, cmd = 11, clk = 8, att = 10; // Digital pins used
int rX = 0, rY = 0, lX = 0, lY = 0; //joystick X and Y values


void setup()
{  Serial.begin(57600);

  error = ps2.config_gamepad(clk, cmd, att, data, false, false); // GamePad(clock(blue), command(orange), attention(Yellow), data(brown), Pressures?, Rumble?)
  if(error == 0)
    Serial.println("Dual Shock PS2 Controller Found");
    
  else if(error == 1)
    Serial.println("No controller found, check wiring");

  else if(error == 2)
    Serial.println("Controller found but not accepting commands");

  else if(error == 3)
    Serial.println("Controller refusing to enter Pressures mode, may not support it. ");
  type = ps2.readType();
    
}


void loop()
{
  if(true)
  {
    ps2.read_gamepad(false, vibrate);
    if(ps2.Button(PSB_RED))
    {
      Serial.println("pressed CIRCLE");
    }
    if(ps2.Button(PSB_GREEN))
    {
      Serial.println("pressed TRIANGLE");
    }
    if(ps2.Button(PSB_PINK))
    {
      Serial.println("pressed SQUARE");
    }
    if(ps2.Button(PSB_BLUE))
    {
      Serial.println("pressed CROSS");
    }
    if(ps2.Button(PSB_PAD_RIGHT))
    {
      Serial.println("RIGHT");
    }
    if(ps2.Button(PSB_PAD_UP))
    {
      Serial.println("UP");
    }
    if(ps2.Button(PSB_PAD_LEFT))
    {
      Serial.println("LEFT");
    }
    if(ps2.Button(PSB_PAD_DOWN))
    {
      Serial.println("DOWN");
    }
    if(ps2.Button(PSB_R1))
    {
      Serial.println("R1");
    }
    if(ps2.Button(PSB_R2))
    {
      Serial.println("R2");
    }
    if(ps2.Button(PSB_L1))
    {
      Serial.println("L1");
    }
    if(ps2.Button(PSB_L2))
    {
      Serial.println("L2");
    }
    if(ps2.Button(PSB_R3))
    {
      Serial.println("rstickB");
    }
    if(ps2.Button(PSB_L3))
    {
      Serial.println("lstickB");
    }
    ////// End of push button checks //////
    
    rX = ps2.Analog(PSS_RX);
    Serial.print("rX = ");
    Serial.print(rX);
    rY = ps2.Analog(PSS_RY);
    Serial.print(",rY = ");
    Serial.print(rY);
  
    lX = ps2.Analog(PSS_LX);
    Serial.print("lX = ");
    Serial.print(lX);  
    lY = ps2.Analog(PSS_LY);
    Serial.print(",lY = ");
    Serial.print(lY);

    Serial.println(" ");
    ////// End of joystick position checks //////
    delay(80);
  }
}
