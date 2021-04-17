#include<PS2X_lib.h>


PS2X ps2;

byte type = 0; // 0 = Unknown, 1 = Dual Shock 
byte vibrate = 0; // vibration motor speed
int error = 0; // error recieved during config
int rX = 0, rY = 0, lX = 0, lY = 0; //joystick X and Y values

int en1_r = 45, en1_l = 47, en2_r = 51, en2_l = 53;
int in1 = 6, in2 = 5, in3 = 3, in4 = 2;

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
  
  digitalWrite(en1_r, HIGH);
  digitalWrite(en1_l, HIGH);
  digitalWrite(en2_r, HIGH);
  digitalWrite(en2_l, HIGH);
  
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

void loop()
{
  ps2.read_gamepad(false, vibrate);

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
