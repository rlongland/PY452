//// ArduinoDAQ
// Kevin Hughes 2012
// Edited by Richard Longland 2016

//// Constants
const int d = 1;
const int analogOutPin = 9;

int outputValue = 0;
int sensorValue = 0;

void setup() {

  // All pins to input
  pinMode(A0, INPUT);
  pinMode(A1, INPUT);
  pinMode(A2, INPUT);
  pinMode(A3, INPUT);
  pinMode(A4, INPUT);
  pinMode(A5, INPUT);

  // Init Serial
  Serial.begin(9600);

}// end setup

void loop() {

//  if(Serial.available()) {

    int signal = Serial.read();
    outputValue = map(signal, 0, 5, 0, 255);
    delay(2);  // wait 2 milliseconds

    sensorValue = analogRead(A0);
    Serial.print(sensorValue); delayMicroseconds(d);
    Serial.print(" ");
    sensorValue = analogRead(A1);
    Serial.print(sensorValue); delayMicroseconds(d);
    Serial.print(" ");
    sensorValue = analogRead(A2);
    Serial.print(sensorValue); delayMicroseconds(d);
    Serial.print(" ");
    sensorValue = analogRead(A3);
    Serial.print(sensorValue); delayMicroseconds(d);
    Serial.print(" ");
    sensorValue = analogRead(A4);
    Serial.print(sensorValue); delayMicroseconds(d);
    Serial.print(" ");
    sensorValue = analogRead(A5);
    Serial.print(sensorValue); delayMicroseconds(d);
    Serial.print("\n");

//  }// end if
}// end loop
