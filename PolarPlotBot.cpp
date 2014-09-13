//====================
//A LIBRARY FOR POLAR COORDINATES DRAWING 'BOT

#include "PolarPlotBot.h"
//#include <math.h>

// moves a chalkWalker or similar bot in concentric circles or a spiral 
// and controls the 'drawing' mechanism
 
PolarPlotBot::PolarPlotBot(float maxRadiusGiven, float startRadius){

  PolarPlotBot(maxRadiusGiven, startRadius, 5,6,9,2);

}

PolarPlotBot::PolarPlotBot(float maxRadiusGiven, float startRadius, 
                           int radiusMotorPin, int angleMotorPin, int drawMotorPin, 
                           int hallSensePin){

  // set up some default vals
 
  radiusMotorPin = radiusMotorPin;  // PWM pin controlling power to radius motor
  angleMotorPin = angleMotorPin;
  drawMotorPin = drawMotorPin;
  hallSensePin = hallSensePin;
  
  angle = 0;   // current state of angle  (radians)
  radius = startRadius; //  current state of radius (cm)
  maxRadius = maxRadiusGiven; //
  // usually use normalized radius, or radius/maxRadius,  rNorm()

  radiusAdvPulseLength = 200;  // this may depend on canvas size
  angleAdvPulseLength = 200;   // may depend on canvas size
  
  radiansPerPulse = PI / 180;   // how much does angle increase when advancing, assume 2 degrees?
  cmPerPulse = 1;  
  
  // is this used? 
  //drawAngle = PI/4; 

  return;
}
 
float PolarPlotBot::rNorm(){
  return radius/maxRadius;
}

void PolarPlotBot::pause(){return;}

void PolarPlotBot::setAngle(float a){
  angle = a;
  return;
}

void PolarPlotBot::setRadius(float r){
  radius = r;
  return;
}

void PolarPlotBot::advance(){
  // move 'forward', increase angle
  analogWrite(angleMotorPin, 235);
  delay(angleAdvPulseLength);    
  analogWrite(angleMotorPin, 0);
  return;
}

void PolarPlotBot::advanceRadius(){
      
  analogWrite(radiusMotorPin, 235);
  delay(radiusAdvPulseLength);    
  analogWrite(radiusMotorPin, 0);
  return;
}


void PolarPlotBot::singleDrop(){
  PolarPlotBot::halfTurn(drawMotorPin, hallSensePin);
  // delay (SHORT_PAUSE);
// oneTurn(pwm_1 ,sensePin_1, 235);
}

void PolarPlotBot::openDraw(){
  PolarPlotBot::fullTurn(drawMotorPin, hallSensePin, 235);
  // delay (SHORT_PAUSE);
// oneTurn(pwm_1 ,sensePin_1, 235);
}

void PolarPlotBot::closeDraw(){}

void PolarPlotBot::halfTurn(int motorPin, int hallSensorPin) { 
  int i;
  int initialHallVal = digitalRead(hallSensorPin);
  
  while (digitalRead(hallSensorPin) == initialHallVal) {
    analogWrite(motorPin, 235);
    delay(40);
    analogWrite(motorPin, 0);
    delay(100);
  }
  
  // move to middle of range of sensor?
  analogWrite(motorPin, 235);
  delay(200);
  analogWrite(motorPin, 0);
  
  return;
}

void PolarPlotBot::fullTurn(int channel_a, int check, int chA_pwr)
{ 
  int i;
  // move out of range of sensor?
 for (i=8;i>1;i--)
  {
  analogWrite(channel_a, chA_pwr);
  delay(40);
  analogWrite(channel_a, 0);
  delay(100);
  digitalRead(check);
 }
 while (digitalRead(check) == 1)
 {
  digitalRead(check);
  analogWrite(channel_a, chA_pwr);
  delay(40);
  analogWrite(channel_a, 0);
  delay(100);
  digitalRead(check);
 }
}

int PolarPlotBot::RhodoneaCurve(float k, float threshold){

  if (radius/maxRadius - cos(k*angle) < threshold){
    return 1;
  }
  
  return 0;

}

int PolarPlotBot::heartCurve(){

  float cosAngle =  cos(angle);
  if( radius/maxRadius < (3 - 2 * sin(angle) + cos(2*angle) - 2 * abs(cosAngle) ) ) {
    return 1;
  }
  
  return 0;

}


int PolarPlotBot::wedge(){

  float cosAngle =  cos(angle);
  if( angle < PI / 8.0 ) {
    return 1;
  }
  
  return 0;

}

