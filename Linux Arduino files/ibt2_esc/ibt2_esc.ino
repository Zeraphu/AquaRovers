/*
IBT-2 Motor Control Board driven by Arduino.
 
Speed and direction controlled by a potentiometer attached to analog input 0.
One side pin of the potentiometer (either one) to ground; the other side pin to +5V
 
Connection to the IBT-2 board:
IBT-2 pin 1 (RPWM) to Arduino pin 5(PWM)
IBT-2 pin 2 (LPWM) to Arduino pin 6(PWM)
IBT-2 pins 3 (R_EN), 4 (L_EN), 7 (VCC) to Arduino 5V pin
IBT-2 pin 8 (GND) to Arduino GND
IBT-2 pins 5 (R_IS) and 6 (L_IS) not connected
*/
 
//int SENSOR_PIN = 0; // center pin of the potentiometer
 
int RPWM= 5; // Arduino PWM output pin 5; connect to IBT-2 pin 1 (RPWM)
int LPWM= 4;
int R_en = 3;
int L_en = 2; // Arduino PWM output pin 6; connect to IBT-2 pin 2 (LPWM)
 
void setup()
{
  pinMode(RPWM, OUTPUT);
  pinMode(LPWM, OUTPUT);
  pinMode(R_en, OUTPUT);
  pinMode(L_en, OUTPUT);
}
 
void loop()
{
  delay(1000);
  digitalWrite(R_en, HIGH);
  digitalWrite(L_en, LOW);
  digitalWrite(RPWM, HIGH);
  digitalWrite(LPWM, LOW);
  delay(1000);
  digitalWrite(R_en, LOW);
  digitalWrite(L_en, HIGH);
  digitalWrite(RPWM, LOW);
  digitalWrite(LPWM, HIGH);
  
}
