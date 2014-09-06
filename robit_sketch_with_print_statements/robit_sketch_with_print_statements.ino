/*
==========PROTOCOL:==========
 To control RIGHT Jaguar, send decimal values in range 20-74 (hex 0x14-0x4A)
 To control LEFT Jaguar, send decimal values in range 75-129 (hex 0x4B-0x81)
 ===NOTE THAT THESE ARE INTEGER VALUES, NOT ASCII CHARACTERS===
 */
#include <avr/interrupt.h>
const int leftJag = 9; //LEFT Jaguar governed by pwm on pin 9
const int rightJag = 10; //RIGHT Jaguar governed by pwm on pin 10
const int jagpwrpin = 5;//using pin 7 as the pwm power reference
const int jaggndpin = 6;//pwm ground reference
const int ledpin = 13;//using the standard LED as a status indicator
//Jag motor speed reference:
const int j_mid = 47; //stopped (hex 0x2F)
const int j_min = 20; //FULL REVERSE (hex 0x14)
const int j_max = 74; //FULL FORWARD (hex 0x4A)
//EMERGENCY STOP VALUE: Stops both Jags (sets them to j_mid) when received:
const int ESTOP = 0; //EMERGENCY STOP
int leftVal, rightVal = 47; //new motor speed settings
//int temp = 0; //temp value for unprocessed bytes received over Serial.
int leftSpeed, rightSpeed; //current speed of the motors

void setup()
{
  //set the PWM frequency for timer 1 to be 122Hz
  TCCR1B = TCCR1B & 0b11111000 | 0x04;
  //setup the PWM reference pins:
  pinMode(leftJag, OUTPUT);
  pinMode(rightJag, OUTPUT);
  pinMode(jagpwrpin, OUTPUT);
  pinMode(jaggndpin, OUTPUT);
  //define the pwm reference voltages
  digitalWrite(jagpwrpin,HIGH);
  digitalWrite(jaggndpin,LOW);
  //start the Serial interface.
  Serial.begin(9600);
  //set the pwm to midscale so the Jaguars don't move at startup:
  analogWrite(leftJag,j_mid);
  analogWrite(rightJag,j_mid);
  leftSpeed, rightSpeed = j_mid; //record the setting of the motors
}

char intBuffer[3];
String intData = "";
int delimiter = (int) '\n';

void loop(){
  int i = intFromSerial(); 
}

int intFromSerial() {
  while (Serial.available()) {
    int ch = Serial.read();
    if (ch==-1) {
      break; //TODO: Handle Error! 
    } else if (ch == delimiter) {
      break; 
    } else {
      intData += (char) ch;
    }
  }
  
  intData.toCharArray(intBuffer, intData.length()+1);
  intData = "";

  int i = atoi(intBuffer);
  Serial.write(intBuffer);
  return i;
}

