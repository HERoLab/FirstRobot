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
const int speed_mid = 47; //stopped (hex 0x2F)
const int speed_min = 20; //FULL REVERSE (hex 0x14)
const int speed_max = 74; //FULL FORWARD (hex 0x4A)
const int motor_diff = 55;

void setup(){
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
  Serial.flush();

  //set the pwm to midscale so the Jaguars don't move at startup:
  analogWrite(leftJag,speed_mid);
  analogWrite(rightJag,speed_mid);
}

int delimiter = (int) '\n';
int leftVal, rightVal = speed_mid; 

void loop(){
  // delay(100);

  if (Serial.available() > 0) {
    int lenBuffer = Serial.available();
    int i = intFromSerial();
    //int i = 50;

    //if (leftVal!=i and rightVal!=i) {
    char intBuffer[lenBuffer];
    itoa(i,intBuffer, 10);
    Serial.write(intBuffer);
    Serial.println(" ");

    //If i is a valid motor speed setting
    if (i >= speed_min and i <= speed_max+speed_mid) { 
      if (i <= speed_max) {
        rightVal = i;
        analogWrite(rightJag, i);
      } else {
        leftVal = i;
        analogWrite(leftJag, i-motor_diff); //Subtract fit the 20 to 74 range of Jaguar PWM signals
      } 
    }

  //}
  }

}

int intFromSerial() {
  String wholeInt = "";
  while (Serial.available()>0){
    int newInt = Serial.read();
    if ( (char) newInt == (char) 'q' ) {
      break;
    } else {
      wholeInt += (char) newInt;
      delay(10);
    }
  }
  return wholeInt.toInt();  
}

