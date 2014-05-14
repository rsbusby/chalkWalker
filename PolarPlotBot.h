//====================
//A LIBRARY FOR POLAR COORDINATES DRAWING 'BOT

#ifndef PolarPlotBot_h
#define PolarPlotBot_h

#if ARDUINO >= 100
#include "Arduino.h"
#else
#include "WProgram.h"
#endif

class PolarPlotBot
{
  // moves a chalkWalker or similar bot in concentric circles or a spiral 
  // and controls the 'drawing' mechanism
 
  public:
   
    PolarPlotBot(float maxRadius, float startRadius);
 
    float rNorm();
    
    void pause();

    void setAngle(float a);

    void setRadius(float r);
    
    void advance();
    
    void advanceRadius();
    
    void openDraw();   // move chalk dropper to open position 
                       // (usually a quarter turn, determined by Hall sensor )
    
    void closeDraw();  // move back to closed position
 
    void OneTurn(int channel_a, int check, int chA_pwr);  // 

    int RhodoneaCurve(float k, float threshold);

    int heartCurve();

 private:

    int radiusMotorPin;  // PWM pin controlling power to radius motor
    int angleMotorPin;
    int drawMotorPin;
    int hallSensePin;
  
    float angle;   // current state of angle (radians)
    float radius; //  current state of radius (cm)
    float maxRadius;  // maximum radius. Size of canvas. 

    float radiusAdvPulseLength;  // milliseconds
    float angleAdvPulseLength; // millis

    float radiansPerPulse;   // how much does angle increase when advancing 
    float cmPerPulse;       // forward distance equivalent for each revolution pulse
  
    float drawAngle;    // angle in radians of the dropping/drawing mechanism
  
};

#endif 
