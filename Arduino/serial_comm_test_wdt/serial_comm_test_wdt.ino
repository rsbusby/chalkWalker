#include <avr/io.h> 
#include <avr/wdt.h>


void setup() {
 Serial.begin(9600); // set the baud rate
  Serial.println("Ready"); // print "Ready" once
  while(!Serial.available()) ;
  char inByte = Serial.read(); // read the incoming data   
  
}

void loop() {
 char inByte = ' ';
 
   // send some numbers through serial
   Serial.print(6.52);
   Serial.print(" ");
   Serial.println(2.33);
//   delay(1000);   
  
  //read from serial
//  Serial.flush() //flush all previous received and transmitted data
  while(!Serial.available()) ;
  if(Serial.available()){ // only send data back if data has been sent
    char inByte = Serial.read(); // read the incoming data   
//    Serial.println(inByte); // send the data back in a new line so that it is not all one long line
  }
//  delay(1000); // delay for a second
}
