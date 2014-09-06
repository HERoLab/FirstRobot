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

int leftVal, rightVal = speed_mid; //new motor speed settings
int leftSpeed, rightSpeed; //current speed of the motors

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

  //set the pwm to midscale so the Jaguars don't move at startup:
  analogWrite(leftJag,speed_mid);
  analogWrite(rightJag,speed_mid);
  leftSpeed, rightSpeed = speed_mid; //record the setting of the motors
}

void loop(){
   delay(500);
   int i = 50;
   analogWrite(rightJag, i);
   analogWrite(leftJag, i);
   //analogWrite(leftJag, i-motor_diff); //Subtract fit the 20 to 74 range of Jaguar PWM signals
}

