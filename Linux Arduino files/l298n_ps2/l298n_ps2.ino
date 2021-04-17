#include<PS2X_lib.h>
PS2X ps2;

byte type = 0; // 0 = Unknown, 1 = Dual Shock 
byte vibrate = 0; // vibration motor speed
int error = 0; // error recieved during config
int data, cmd, clock, att; // Digital pins used
int rX = 0, rY = 0, lX = 0, lY = 0; //joystick X and Y values
int en1_r =  45, en1_l = 47, en2_r = 51, en2_l = 53, in1 = 6, in2 = 5, in3 = 4, in4 = 3;


void setup()
{  Serial.begin(57600);
    pinMode(in1, OUTPUT);
    pinMode(in2, OUTPUT);
    pinMode(in3, OUTPUT);
    pinMode(in4, OUTPUT);
    pinMode(en1_r, OUTPUT);
    pinMode(en1_l, OUTPUT);
    pinMode(en2_r, OUTPUT);
    pinMode(en2_l, OUTPUT);
    
    digitalWrite(en1_r, HIGH);
    digitalWrite(en1_l, HIGH);
    digitalWrite(en2_r, HIGH);
    digitalWrite(en2_l, HIGH);
    
  error = ps2.config_gamepad(8, 11, 10, 12, false, false); // GamePad(clock(blue), command(orange), attention(Yellow), data(brown), Pressures?, Rumble?)
  if(error == 0)
    Serial.println("Dual Shock PS2 Controller Found");
    
  else if(error == 1)
    Serial.println("No controller found, check wiring");

  else if(error == 2)
    Serial.println("Controller found but not accepting commands");

  else if(error == 3)
    Serial.println("Controller refusing to enter Pressures mode, may not support it. ");
  type = ps2.readType();
  Serial.println(type);
    
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
      digitalWrite(in1, HIGH);
      digitalWrite(in2, LOW);
      digitalWrite(in3, HIGH);
      digitalWrite(in4, LOW);
    }
    if(ps2.Button(PSB_PINK))
    {
      Serial.println("pressed SQUARE");
      while(ps2.Button(PSB_PINK))
      {
      
      }
    }
    if(ps2.Button(PSB_BLUE))
    {
      Serial.println("pressed CROSS");
      analogWrite(en1_r, 255);
      analogWrite(en1_l, 255);
      analogWrite(en2_r, 255);
      analogWrite(en2_l, 255);
      digitalWrite(in1, LOW);
      digitalWrite(in2, HIGH);
      digitalWrite(in3, LOW);
      digitalWrite(in4, HIGH);
    }
    if(ps2.Button(PSB_PAD_RIGHT))
    {
      Serial.println("RIGHT");
      //analogWrite(en1_r, 255);
      //analogWrite(en1_l, 255);
      analogWrite(en2_r, 255);
      analogWrite(en2_l, 255);
      digitalWrite(in3, HIGH);
      digitalWrite(in4, LOW);
      
    }
    if(ps2.Button(PSB_PAD_UP))
    {
      Serial.println("UP");
      analogWrite(en1_r, 255);
      analogWrite(en1_l, 255);
      //analogWrite(en2_r, 255);
      //analogWrite(en2_l, 255);
      digitalWrite(in1, HIGH);
      digitalWrite(in2, LOW);

    }
    if(ps2.Button(PSB_PAD_LEFT))
    {
      Serial.println("LEFT");
      //analogWrite(en1_r, 255);
      //analogWrite(en1_l, 255);
      analogWrite(en2_r, 255);
      analogWrite(en2_l, 255);

      digitalWrite(in3, LOW);
      digitalWrite(in4, HIGH);
    }
    if(ps2.Button(PSB_PAD_DOWN))
    {
      Serial.println("DOWN");
      analogWrite(en1_r, 255);
      analogWrite(en1_l, 255);
      //analogWrite(en2_r, 255);
      //analogWrite(en2_l, 255);
      digitalWrite(in1, LOW);
      digitalWrite(in2, HIGH);
      
    }
    if(ps2.Button(PSB_R1))
    {
      Serial.println("R");
      digitalWrite(in1, LOW);
      digitalWrite(in2, LOW);
      digitalWrite(in3, LOW);
      digitalWrite(in4, LOW);
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
