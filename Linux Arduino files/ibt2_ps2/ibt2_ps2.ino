
#include<PS2X_lib.h>
PS2X ps2;

byte type = 0; // 0 = Unknown, 1 = Dual Shock 
byte vibrate = 0; // vibration motor speed
int error = 0; // error recieved during config
//int data, cmd, clock, att; // Digital pins used
int rX = 0, rY = 0, lX = 0, lY = 0; //joystick X and Y values

void setup()
{
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
  pinMode(7, OUTPUT);

  pinMode(3, OUTPUT);
  digitalWrite(3, HIGH);

  digitalWrite(4, LOW);
  digitalWrite(5, LOW);
  digitalWrite(6, LOW);
  digitalWrite(7, LOW);

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
int en = 0;
void loop()
{
  if(Serial.available())
  {
    en = ps2.Analog(PSS_LY);
    en = map(en, 0,255,0,1023);
    analogWrite(A0, en);
    if(ps2.Analog(PSS_RX)>125)
    {
      digitalWrite(4, HIGH);
    }
    if(ps2.Analog(PSS_RY)<121)
    {
      digitalWrite(5, HIGH);
    }
    else
    {
      digitalWrite(4, LOW);
      digitalWrite(5, LOW);
    }
  }
}
