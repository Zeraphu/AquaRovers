#include<PS2X_lib.h>
PS2X ps2;

byte type = 0; // 0 = Unknown, 1 = Dual Shock 
byte vibrate = 0; // vibration motor speed
int error = 0; // error recieved during config
//int clock, cmd, clo, att; // Digital pins used
int rX = 0, rY = 0, lX = 0, lY = 0; //joystick X and Y values

int en1_r = 45, en1_l = 47, en2_r = 51, en2_l = 53;
int in1 = 6, in2 = 5, in3 = 3, in4 = 2;

int a_enr = 41, a_enl = 39, a_vcc = 22;
int a_in1 = 31, a_in2 = 33;
//int b_in1 = 40, b_in2 = 44, b_in3 = 7, b_in4 = 4;

int red_on = 38, red_off = 40, green_on = 44, green_off = 46;

void setup()
{
  pinMode(en1_r, OUTPUT);
  pinMode(en1_l, OUTPUT);
  pinMode(en2_r, OUTPUT);
  pinMode(en2_l, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
  
  pinMode(a_enr, OUTPUT);
  pinMode(a_enl, OUTPUT);
  pinMode(a_in1, OUTPUT);
  pinMode(a_in2, OUTPUT);
  pinMode(a_vcc, OUTPUT);
  
  pinMode(b_in1, OUTPUT);
  pinMode(b_in2, OUTPUT);
  pinMode(b_in3, OUTPUT);
  pinMode(b_in4, OUTPUT);
  
  
  digitalWrite(en1_r, HIGH);
  digitalWrite(en1_l, HIGH);
  digitalWrite(en2_r, HIGH);
  digitalWrite(en2_l, HIGH);
  
  digitalWrite(a_enr, HIGH);
  digitalWrite(a_enl, HIGH);
  digitalWrite(a_vcc, HIGH);
  
  digitalWrite(red_on, LOW);
  digitalWrite(red_off, LOW);
  digitalWrite(green_on, LOW);
  digitalWrite(green_off, LOW);
  
  
  Serial.begin(57600);
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
}

int y;
void loop()
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
      digitalWrite(red_on, HIGH);
      digitalWrite(red_off, LOW);
      digitalWrite(green_on, LOW);
      digitalWrite(green_off, LOW);
    
    }
    else if(ps2.Button(PSB_PAD_UP))
    {
      Serial.println("UP");
      digitalWrite(red_on, HIGH);
      digitalWrite(red_off, LOW);
      digitalWrite(green_on, HIGH);
      digitalWrite(green_off, LOW);
    
    }
    else if(ps2.Button(PSB_PAD_LEFT))
    {
      //Serial.println("LEFT");
      //digitalWrite(a_in1, LOW);
      //digitalWrite(a_in2, HIGH);
      digitalWrite(red_on, LOW);
      digitalWrite(red_off, LOW);
      digitalWrite(green_on, HIGH);
      digitalWrite(green_off, LOW);
    }
    else if(ps2.Button(PSB_PAD_DOWN))
    {
      Serial.println("DOWN");
      //digitalWrite(a_in1, HIGH);
      //digitalWrite(a_in2, LOW);
      digitalWrite(red_on, LOW);
      digitalWrite(red_off, LOW);
      digitalWrite(green_on, LOW);
      digitalWrite(green_off, LOW);
    
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
  if(true)
  {
    rX = ps2.Analog(PSS_RX);
    Serial.print(rX);
    if(rX>125)
    {
      analogWrite(en1_r, 1023);
      analogWrite(en1_l, 1023);
      analogWrite(en2_r, 255);
      analogWrite(en2_l, 255);
      digitalWrite(in1, HIGH);
      digitalWrite(in2, LOW);
      //digitalWrite(in3, LOW);
      //digitalWrite(in4, LOW);
    }
    else if(rX<121)
    {
      analogWrite(en1_r, 1023);
      analogWrite(en1_l, 1023);
      analogWrite(en2_r, 255);
      analogWrite(en2_l, 255);
      digitalWrite(in1, LOW);
      digitalWrite(in2, HIGH);
      //digitalWrite(in3, LOW);
      //digitalWrite(in4, LOW);
    }
    else
    {
      digitalWrite(in1, LOW);
      digitalWrite(in2, LOW);
      //digitalWrite(in3, LOW);
      //digitalWrite(in4, LOW);
    }

    rY = ps2.Analog(PSS_RY);
    Serial.print(',');
    Serial.println(rY);
    if(rY>125)
    {
      analogWrite(en1_r, 255);
      analogWrite(en1_l, 255);
      analogWrite(en2_r, 1023);
      analogWrite(en2_l, 1023);
      //digitalWrite(in1, LOW);
      //digitalWrite(in2, LOW);
      digitalWrite(in3, LOW);
      digitalWrite(in4, HIGH);
    }
    else if(rY<121)
    {
      analogWrite(en1_r, 255);
      analogWrite(en1_l, 255);
      analogWrite(en2_r, 1023);
      analogWrite(en2_l, 1023);
      //digitalWrite(in1, LOW);
      //digitalWrite(in2, LOW);
      digitalWrite(in3, HIGH);
      digitalWrite(in4, LOW);
    }
    else
    {
      //digitalWrite(in1, LOW);
      //digitalWrite(in2, LOW);
      digitalWrite(in3, LOW);
      digitalWrite(in4, LOW);
    }
  }
  delay(20);
}
