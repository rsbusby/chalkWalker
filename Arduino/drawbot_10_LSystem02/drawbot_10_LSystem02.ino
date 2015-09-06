  // AFMotor_MultiStepper.pde
// -*- mode: C++ -*-
//
// Control both Stepper motors at the same time with different speeds
// and accelerations. 
// Requires the AFMotor library (https://github.com/adafruit/Adafruit-Motor-Shield-library)

// This file is an attempt to do more complicated L-system type recursive structure to 
//  approximate organic-esque branching lines

#include <AccelStepper.h>
#include <AFMotor.h>

// use centimeters as units
float c = 71.5;
float diam1 = 0.92;
float diam2 = 0.89;

float xa = 0;
float ya = 0;

float cx;
float cy;

int maxLevel = 5;
float yDel = 6;

int ii = 0;

// two stepper motors one on each port
long stepsPerRot =200;
AF_Stepper motor1(stepsPerRot, 1);
AF_Stepper motor2(stepsPerRot, 2);

// you can change these to DOUBLE or INTERLEAVE or MICROSTEP!
// wrappers for the first motor!
void forwardstep1() {  
  motor1.onestep(FORWARD, SINGLE);
}
void backwardstep1() {  
  motor1.onestep(BACKWARD, SINGLE);
}
// wrappers for the second motor!
void forwardstep2() {  
  motor2.onestep(FORWARD, SINGLE);
}
void backwardstep2() {  
  motor2.onestep(BACKWARD, SINGLE);
}


// motor 1 on the right
// Motor shield has two motor ports, now we'll wrap them in an AccelStepper object
AccelStepper stepper1(forwardstep1, backwardstep1);
//AccelStepper stepper2(forwardstep2, backwardstep2);
//AccelStepper stepper1(backwardstep1, forwardstep1);
AccelStepper stepper2(backwardstep2, forwardstep2);


long maxSteps1 = 800;
long maxSteps2 = 400;

int maxSpeed1 = 40;
int maxSpeed2 = 40;

float xCal[4]; // = [30., 40., 40., 30.]
float yCal[4]; // = [30., 30., 40., 40.]

float x0;
float y0;
// global coords
float xx, yy;

//global angle
float a;

///////////////////////////////////
// SETUP
/////////////////////////////////
void setup()
{  
  
  Serial.begin(9600);
  delay(4000);
//  randomSeed(analogRead(1));

  Serial.println("Start");

  // set up initial coords if both threads are the length of the inter-motor distance
  x0 = 0.5*c;
  y0 = 0.87 * c;
  xx = x0;
  yy = y0;

  stepper1.setMaxSpeed(100.0);
  stepper1.setAcceleration(150.0);
  stepper1.setCurrentPosition(getStepsFromDist(c, diam1));
    
  stepper2.setMaxSpeed(100.0);
  stepper2.setAcceleration(150.0);
  stepper2.setCurrentPosition(getStepsFromDist(c, diam2));
  
  // 'center'
  float xc= -3.0;
  float yc = 10.0;
  goToXY(xc, yc);
  xx=xc;
  yy=yc;
  a = -PI/2;
  Serial.println("centered");

  // yo fractals yo
  gSimple(4, 1.6, 0.4, false);

}

////////////////////////////////
// main loop
//////////////////////////////
void loop()
{
  // empty on purpose 
}


void gSimple(int order, float dist, float angle, boolean returnFlag){
  // resursive kernel of L- fractal  
  // globals for now
  //xx,yy,a
  
  Serial.print("order ");
  Serial.println(order);
   if (order == 0){
      forwardLine(dist, a);
   } 
   else{
   
     gSimple(order -1, dist, angle, false);
     
     a = rotateLeft(a, angle);
     gSimple(order -1, dist, angle, true);
     a  = rotateRight(a, angle);
  
     gSimple(order -1, dist, angle, false);
  
     a = rotateRight(a, angle);
     gSimple(order -1, dist, angle, true);
     a = rotateLeft(a, angle);

  }
  if(returnFlag){
     for(int k =0;k<pow(2,order);k++){
       backwardLine(dist,a);
     }
  }
   
   return; 
    
}

float rotateLeft(float dirAngle, float alpha){
   dirAngle = dirAngle - alpha;
   return dirAngle;
}

float rotateRight(float dirAngle, float alpha){
   dirAngle = dirAngle + alpha;
  return dirAngle;
}

void forwardLine(float dist, float dirAngle){
  float x= xx;
  float y=yy;
  float dx = cos(dirAngle) * dist;
  float dy = sin(dirAngle) * dist;

// 
//  line(x, y, x  + dx, y + dy);  // for Processing

  xx = x+ dx;
  yy = y+dy;

  Serial.print(xx);
  Serial.print("  ");
  Serial.println(yy);
  
  goToXY(xx,yy);
 
  return;
}

void backwardLine(float dist, float dirAngle){
 forwardLine(-dist,dirAngle);
}




void continueTillTarget(){
  
 while (stepper2.distanceToGo() != 0 and stepper1.distanceToGo() != 0){
    stepper1.run();
    stepper2.run();
 }
  
}

void goToXY(float x, float y){
  
  
  x = x + x0;
  y = y0 - y ;  // y was flipped
  
//  Serial.print("X Y Current pos ");
//  Serial.print(x);
//  Serial.print(", ");
//  Serial.println(y);
//  
//  Serial.print("X Y Going to ");
//  Serial.print(x);
//  Serial.print(", ");
//  Serial.println(y);
//  
  float L1 = getL1FromXY(x, y);
  float L2 = getL2FromXY(x, y);
//  
//  Serial.print("L1 L2 Going to ");
//  Serial.print(L1);
//  Serial.print(", ");
//  Serial.println(L2);

  int steps1 = (int) getStepsFromDist(L1, diam1);
  int steps2 = (int) getStepsFromDist(L2, diam2);
  
//  Serial.print("Absolute step position: ");
//  Serial.print(steps1);
//  Serial.print(", ");
//  Serial.println(steps2);

  int stepsToGo1 = abs(steps1 - stepper1.currentPosition() );
  int stepsToGo2 = abs(steps2 - stepper2.currentPosition() );

//  Serial.print("Steps to Go:  ");
//  Serial.print(stepsToGo1);
//  Serial.print(", ");
//  Serial.println(stepsToGo2);

  float speedRatio1to2 = 1;
  if (stepsToGo2 != 0 && stepsToGo1 != 0){
    speedRatio1to2 = (float) stepsToGo1 / (float) stepsToGo2;
//    Serial.print("speed ratio: ");  
//    Serial.println(speedRatio1to2);

  }
  
  stepper1.moveTo(steps1);
  stepper2.moveTo(steps2);

  float baseSpeed = 40;
  float baseAccel = 200;

  float max1 = baseSpeed;
  float max2 = baseSpeed;
  float accel1 = baseAccel;
  float accel2 = baseAccel;

  if(speedRatio1to2 < 1){

    max1 = baseSpeed * speedRatio1to2;
    accel1 = baseAccel * speedRatio1to2;
    if (max1 > baseSpeed){
     max1 = baseSpeed;
     accel1 = baseAccel;
    }
  }
  else{
    
    max2 = baseSpeed / speedRatio1to2;
    accel2 = baseAccel / speedRatio1to2;
    if (max2 > baseSpeed){
      max2 = baseSpeed;
      accel2 = baseAccel;
    }
  }

//  Serial.print("speeds ::");
//  Serial.print(max1);
//  Serial.print(", ");
//  Serial.println(accel1);
//  Serial.print("       ::");
//
//  Serial.print(max2);
//  Serial.print(", ");
//  Serial.println(accel2);
//  Serial.println("");

 
//  Serial.print("dtg 00 :");
//
//    Serial.print(stepper1.distanceToGo());
//    Serial.print("   ");
//    Serial.println(stepper2.distanceToGo());
  
  int dir1 = getDirection(stepper1.distanceToGo() );
  int dir2 = getDirection(stepper2.distanceToGo() );

//
// Serial.print("DIRECTION : ");
//  Serial.print(dir1);
//  Serial.print("  ");
//
//  Serial.println(dir2);


  stepper1.setSpeed(max1 * dir1);
  stepper2.setSpeed(max2 * dir2);


//  stepper1.setMaxSpeed(max1);
//  stepper1.setAcceleration(accel1);
//  stepper2.setMaxSpeed(max2);
//  stepper2.setAcceleration(accel2);

  int hh;
  while(stepper1.distanceToGo() * dir1 > 0 || stepper2.distanceToGo() * dir2 > 0){
//    Serial.print("stepping, ");
//    Serial.print(hh);
//    Serial.print("   , dtg:");
//
//    Serial.print(stepper1.distanceToGo());
//    Serial.print("   ");
//    Serial.println(stepper2.distanceToGo());
    stepper1.runSpeed();
    stepper2.runSpeed();
  

  }

}


int getDirection(int dist){
    if (dist > 0)  
      return 1;
    else   
      return -1;
}

float getStepsFromDist(float dcm, float diam){
  
  float circ = diam * 3.1415927;
  return dcm / circ * stepsPerRot;
  
}

float getL2FromXY(float x,float y){
 // c is the motor spacing 
  return sqrt(x*x+y*y);
}

float getL1FromXY(float x, float y){
 // c is the motor spacing 
   float x2 = c-x;
  return sqrt(x2*x2 + y*y);
}



void upRight(float d, float ratio, int level, float x, float y){
 if (level < maxLevel){
    
     up(d,x,y);
     y = y -d;
     right(d,x,y);
     x = x +d;
     downRight(d*ratio, ratio, level + 1, x, y);
     upRight(d*ratio, ratio, level +1, x,y);
     left(d,x,y);
     x = x-d;
     down(d,x,y);
     y = y+d;
     
 } 
  return;
}

void upLeft(float d, float ratio, int level, float x, float y){
 if (level < maxLevel){
    
     up(d,x,y);
     y=y-d;
     left(d,x,y);
     x=x-d;
     downLeft(d*ratio, ratio, level + 1,x,y);
     upLeft(d*ratio, ratio, level +1,x,y);
     right(d,x,y);
     x=x+d;
     down(d, x,y);
     y=y+d;
     
 } 
  return;
}

void downLeft(float d, float ratio, int level,float x, float y){
  upRight(-d, ratio, level,x,y); 
  return;
}

void downRight(float d, float ratio, int level, float x, float y){
  upLeft(-d, ratio, level,x,y); 
  return;
}

void up(float d,float x, float y){
  
  goToXY(x,y-1.6*d);
  return;
}

void right(float d,float x, float y){
  
  goToXY(x+d,y);
  return;
}

void down(float d,float x, float y){
  up(-d,x,y);
  return;
}

void left(float d,float x, float y){
  right(-d,x,y);
  return;
}


