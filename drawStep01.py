#!/usr/bin/python
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_StepperMotor
import time
import atexit
import threading
import random
from math import sqrt, pi, cos, sin

# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT()

# create empty threads (these will hold the stepper 1 and 2 threads)
st1 = threading.Thread()
st2 = threading.Thread()


# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
	mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

atexit.register(turnOffMotors)

myStepper1 = mh.getStepper(200, 1)  	# 200 steps/rev, motor port #1
myStepper2 = mh.getStepper(200, 2)  	# 200 steps/rev, motor port #1
myStepper1.setSpeed(60)  		# 30 RPM
myStepper2.setSpeed(60)  		# 30 RPM


stepstyles = [Adafruit_MotorHAT.SINGLE, Adafruit_MotorHAT.DOUBLE, Adafruit_MotorHAT.INTERLEAVE, Adafruit_MotorHAT.MICROSTEP]

def stepper_worker(stepper, numsteps, direction, style):
	#print("Steppin!")
	stepper.step(numsteps, direction, style)
	#print("Done")



    

# yo fractals yo
gSimple(4, 1.6, 0.4, false)






    
# while (True):
# 	if not st1.isAlive():
# 		randomdir = random.randint(0, 1)
# 		print("Stepper 1"),
# 		if (randomdir == 0):
# 			dir = Adafruit_MotorHAT.FORWARD
# 			print("forward"),
# 		else:
# 			dir = Adafruit_MotorHAT.BACKWARD
# 			print("backward"),
# 		randomsteps = random.randint(10,50)
# 		print("%d steps" % randomsteps)
# 		st1 = threading.Thread(target=stepper_worker, args=(myStepper1, randomsteps, dir, stepstyles[random.randint(0,3)],))
# 		st1.start()

# 	if not st2.isAlive():
# 		print("Stepper 2"),
# 		randomdir = random.randint(0, 1)
# 		if (randomdir == 0):
# 			dir = Adafruit_MotorHAT.FORWARD
# 			print("forward"),
# 		else:
# 			dir = Adafruit_MotorHAT.BACKWARD
# 			print("backward"),

# 		randomsteps = random.randint(10,50)		
# 		print("%d steps" % randomsteps)

# 		st2 = threading.Thread(target=stepper_worker, args=(myStepper2, randomsteps, dir, stepstyles[random.randint(0,3)],))
# 		st2.start()


        
class drawbot(Object):
    """ Semi-port of Arduino code for wall drawing bot"""

    def __init__(self):
        self.x0 = 0
        self.y0 = 0
        
        # use centimeters as units
        self.motor_sep = 71.5;
        self.diam1 = 0.92;
        self.diam2 = 0.89;




    def gSimple(self, order, dist, angle, returnFlag):
        # resursive kernel of L- fractal  
        # globals for now
        #xx,yy,a

        print("order ");
        print(order);
        if order == 0:
            forwardLine(dist, a)
        else:
            gSimple(order -1, dist, angle, false);

            a = rotateLeft(a, angle);
            gSimple(order -1, dist, angle, true);
            a  = rotateRight(a, angle);

            gSimple(order -1, dist, angle, false);

            a = rotateRight(a, angle);
            gSimple(order -1, dist, angle, true);
            a = rotateLeft(a, angle);

        if returnFlag:
            for k in range(0, pow(2, order)):
               backwardLine(dist,a)

        return; 


    def rotateLeft(self,  dirAngle,  alpha):
        dirAngle = dirAngle - alpha;
        return dirAngle;
    

    def rotateRight(self,  dirAngle,  alpha):
        dirAngle = dirAngle + alpha;
        return dirAngle;
    

    def forwardLine(self,  dist,  dirAngle):
        x= xx;
        y=yy;
        dx = cos(dirAngle) * dist;
        dy = sin(dirAngle) * dist;

        #
        line(x, y, x  + dx, y + dy);  # for Processing

        xx = x+ dx;
        yy = y+dy;

        print(xx);
        print("  ");
        print(yy);

        goToXY(xx,yy);

        return;


    def backwardLine(self,  dist,  dirAngle):
        forwardLine(-dist,dirAngle)
    

    def getDirection(self, dist):
        if dist > 0:  
          return 1
        else:   
          return -1

    def getStepsFromDist(self, dcm, diam):
      circ = diam * pi;
      return dcm / circ * stepsPerRot;

    def getL2FromXY(self, x, y):
      #c is the motor spacing
      return sqrt(x*x+y*y)
    

    def getL1FromXY(self, x, y):
        # c is the motor spacing 
        x2 = c-x;
        return sqrt(x2*x2 + y*y)
        
        
    def goToXY(self, x, y):
        """x, y are s """
        x = x + self.x0
        y = self.y0 - y  #y was flipped
  
        print("X Y Current pos ");
        print(x);
        print(", ");
        print(y);
  
        print("X Y Going to ");

        L1 = getL1FromXY(x, y);
        L2 = getL2FromXY(x, y);
# #  
# #  print("L1 L2 Going to ");
# #  print(L1);
# #  print(", ");
# #  print(L2);

        steps1 = int(getStepsFromDist(L1, diam1))
        steps2 = int(getStepsFromDist(L2, diam2))
  
# #  print("Absolute step position: ");
# #  print(steps1);
# #  print(", ");
# #  print(steps2);

        stepsToGo1 = abs(steps1 - stepper1.currentstep )
        stepsToGo2 = abs(steps2 - stepper2.currentstep )

# #  print("Steps to Go:  ");
# #  print(stepsToGo1);
# #  print(", ");
# #  print(stepsToGo2);

        speedRatio1to2 = 1
        if stepsToGo2 != 0 and stepsToGo1 != 0:
            speedRatio1to2 = float(stepsToGo1 / float(stepsToGo2))
        print("speed ratio: ");  
        print(speedRatio1to2);
  
        stepper1.moveTo(steps1);
        stepper2.moveTo(steps2);

        baseSpeed = 40
        baseAccel = 200

        max1 = baseSpeed;
        max2 = baseSpeed;
        accel1 = baseAccel;
        accel2 = baseAccel;

        if(speedRatio1to2 < 1):

            max1 = baseSpeed * speedRatio1to2;
            accel1 = baseAccel * speedRatio1to2;
            if (max1 > baseSpeed):
                max1 = baseSpeed;
                accel1 = baseAccel;
        else:
            max2 = baseSpeed / speedRatio1to2;
            accel2 = baseAccel / speedRatio1to2;
            if (max2 > baseSpeed):
                max2 = baseSpeed;
                accel2 = baseAccel;


# #  print("speeds ::");
# #  print(max1);
# #  print(", ");
# #  print(accel1);
# #  print("       ::");
# #
# #  print(max2);
# #  print(", ");
# #  print(accel2);
# #  print("");

 
# #  print("dtg 00 :");
# #
# #    print(stepper1.distanceToGo());
# #    print("   ");
# #    print(stepper2.distanceToGo());
  
        dir1 = getDirection(stepper1.distanceToGo() );
        dir2 = getDirection(stepper2.distanceToGo() );

# #
# # print("DIRECTION : ");
# #  print(dir1);
# #  print("  ");
# #
# #  print(dir2);


        stepper1.setSpeed(max1 * dir1);
        stepper2.setSpeed(max2 * dir2);


# #  stepper1.setMaxSpeed(max1);
# #  stepper1.setAcceleration(accel1);
# #  stepper2.setMaxSpeed(max2);
# #  stepper2.setAcceleration(accel2);

        while (stepper1.distanceToGo() * dir1 > 0) or (stepper2.distanceToGo() * dir2 > 0):
# #    print("stepping, ");
# #    print("   , dtg:");
# #
# #    print(stepper1.distanceToGo());
# #    print("   ");
# #    print(stepper2.distanceToGo());
            stepper1.runSpeed();
            stepper2.runSpeed();
  


    def upRight(self, d, ratio, level, x, y):
        if (level < maxLevel):

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


        return
    

    def upLeft(self, d, ratio, level, x, y):
        if (level < maxLevel):

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


        return


    def downLeft(self, d, ratio, level,x, y):
        upRight(-d, ratio, level,x,y); 
        return
    

    def downRight(self, d, ratio, level, x, y):
        upLeft(-d, ratio, level,x,y); 
        return
    

    def up(self, d,x, y):

        goToXY(x,y-1.6*d);
        return
    

    def right(self, d,x, y):

      goToXY(x+d,y);
      return
    

    def down(self, d,x, y):
      up(-d,x,y);
      return
    

    def left(self, d,x, y):
      right(-d,x,y);
      return
    

