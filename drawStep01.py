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

print "st1"
print st1

# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
	mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

atexit.register(turnOffMotors)

#myStepper1 = mh.getStepper(200, 1)  	# 200 steps/rev, motor port #1
#myStepper2 = mh.getStepper(200, 2)  	# 200 steps/rev, motor port #1
#myStepper1.setSpeed(60)  		# 30 RPM
#myStepper2.setSpeed(60)  		# 30 RPM


stepstyles = [Adafruit_MotorHAT.SINGLE, Adafruit_MotorHAT.DOUBLE, Adafruit_MotorHAT.INTERLEAVE, Adafruit_MotorHAT.MICROSTEP]

def stepper_worker(stepper, numsteps, direction, style):
	#print("Steppin!")
	stepper.step(numsteps, direction, style)
	#print("Done")



    
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


        
class drawbot(object):
    """ Semi-port of Arduino code for wall drawing bot"""

    def __init__(self):


        self.st1 = threading.Thread()
	self.st2 = threading.Thread()

        # use centimeters as units
        self.motor_sep = 71.5;
	self.c = self.motor_sep
        self.diam1 = 0.92;
        self.diam2 = 0.89;

	self.stepsPerRot = 200

	# global angle
	self.a = pi/2.0

        self.x0 = 0.5*self.c
        self.y0 = -0.87*self.c

	print "initial (x,y): (" + str(self.x0) + ", " + str(self.y0) + ")" 

	self.xx = self.x0
	self.yy = self.y0

	self.stepper1 = mh.getStepper(200, 1)  	# 200 steps/rev, motor port #1
	self.stepper2 = mh.getStepper(200, 2)  	# 200 steps/rev, motor port #1
	self.stepper1.setSpeed(60)  		# 30 RPM
	self.stepper2.setSpeed(60)  		# 30 RPM


	self.curStep1 = int(self.getStepsFromDist(self.c, self.diam1))
	self.curStep2 = int(self.getStepsFromDist(self.c, self.diam2))



	print "initial initial steps: " + str(self.stepper1.currentstep)
	

    def gSimple(self, order, dist, angle, returnFlag):
        # resursive kernel of L- fractal  
        # globals for now
        #xx,yy,a

        print "order " + str(order)

        if order == 0:
            self.forwardLine(dist, self.a)
        else:
            self.gSimple(order -1, dist, angle, False);

            self.a = self.rotateLeft(self.a, angle);
            self.gSimple(order -1, dist, angle, True);
            self.a  = self.rotateRight(self.a, angle);

            self.gSimple(order -1, dist, angle, False);

            self.a = self.rotateRight(self.a, angle);
            self.gSimple(order -1, dist, angle, True);
            self.a = self.rotateLeft(self.a, angle);

        if returnFlag:
            for k in range(0, pow(2, order)):
               self.backwardLine(dist, self.a)

        return


    def rotateLeft(self,  dirAngle,  alpha):
        dirAngle = dirAngle - alpha;
        return dirAngle;
    

    def rotateRight(self,  dirAngle,  alpha):
        dirAngle = dirAngle + alpha;
        return dirAngle;
    

    def forwardLine(self,  dist,  dirAngle):
        x = self.xx;
        y = self.yy;
        dx = cos(dirAngle) * dist;
        dy = sin(dirAngle) * dist;

        #
        # line(x, y, x  + dx, y + dy);  # for Processing

        self.xx = x+ dx;
        self.yy = y+dy;

	print str(dx) + " " + str(dy)
        print str(self.xx) + "  " + str(self.yy)

        self.goToXY(self.xx,self.yy);

        return;


    def backwardLine(self,  dist,  dirAngle):
        self.forwardLine(-dist,dirAngle)
    

    def getDirection(self, dist):
        if dist > 0:  
          return 1
        else:   
          return -1

    def getStepsFromDist(self, dcm, diam):
      circ = diam * pi;
      return dcm / circ * self.stepsPerRot;

    def getL2FromXY(self, x, y):
      #c is the motor spacing
      return sqrt(x*x+y*y)
    

    def getL1FromXY(self, x, y):
        # c is the motor spacing 
        x2 = self.c-x;
        return sqrt(x2*x2 + y*y)
        
        
    def goToXY(self, x, y):
        """x, y are s """

	print self.st1
	print "go to: " +str(x) + " " + str(y)

        #x = x - self.x0
        #y = self.y0 - y  #y was flipped
  
        print("X Y Current pos ");
        print(x);
        print(y);
  
        print("X Y Going to ");

        L1 = self.getL1FromXY(x, y);
        L2 = self.getL2FromXY(x, y);
# #  
	print("L1 L2 Going to ");
	print(L1);
	print(L2);


        steps1 = int(self.getStepsFromDist(L1, self.diam1))
        steps2 = int(self.getStepsFromDist(L2, self.diam2))
  

	print("Absolute step position: ");
	print(steps1);
# #  print(", ");
	print(steps2);

	stepsToGoSigned1 = (steps1 - self.curStep1 )
	stepsToGoSigned2 = (steps2 - self.curStep2 )

        stepsToGo1 = abs(steps1 - self.curStep1 )
        stepsToGo2 = abs(steps2 - self.curStep2 )

	if stepsToGoSigned1 >= 0:
            dir1 = Adafruit_MotorHAT.FORWARD
	    dirSign1 = 1
	else:
            dir1 = Adafruit_MotorHAT.BACKWARD
	    dirSign1 = -1
	if stepsToGoSigned2 >= 0:
            dir2 = Adafruit_MotorHAT.FORWARD
	    dirSign2 = 1
	else:
            dir2 = Adafruit_MotorHAT.BACKWARD
	    dirSign2 = -1

	print("Steps to Go:  ");
	print(stepsToGo1);
	print(", ");
	print(stepsToGo2);

        speedRatio1to2 = 1
        if stepsToGo2 != 0 and stepsToGo1 != 0:
            speedRatio1to2 = float(stepsToGo1 / float(stepsToGo2))
        print("speed ratio: ");  
        print(speedRatio1to2);
  
        #myStepper1.moveTo(steps1);
        #myStepper2.moveTo(steps2);

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


	print("speeds ::");
	print(max1);
# #  print(", ");
	print(max2);

	#print "DIRS: " + str(dir1) + " " + str(dir2)
 
# #  print("dtg 00 :");
# #
# #    print(myStepper1.distanceToGo());
# #    print("   ");
# #    print(myStepper2.distanceToGo());
  
        #dir1 = self.getDirection(steps1 );
        #dir2 = self.getDirection(steps2 );

# #
# # print("DIRECTION : ");
# #  print(dir1);
# #  print("  ");
# #
# #  print(dir2);

	print " " 
	print stepsToGo1
	print dir1
	print stepstyles[1]
	import time
	stepsToGo1 = 30
	stepsToGo2 = 20
        self.stepper1.setSpeed(30);
        self.stepper2.setSpeed(3);
	while self.st1.isAlive() or self.st2.isAlive(): 
            print "waitung"
            time.sleep(1)
	if not self.st1.isAlive() and not self.st2.isAlive():
            print "initial steps: " + str(self.stepper1.currentstep)
            self.st1 = threading.Thread(target=stepper_worker, args=(self.stepper1, stepsToGo1, dir1, stepstyles[1],))
	    self.st2 = threading.Thread(target=stepper_worker, args=(self.stepper2, stepsToGo2, dir2, stepstyles[1],))
	    self.st1.start()

	    self.st2.start()
	    print "old steps: " + str(self.curStep1) + " " + str(self.curStep2)
	    self.curStep1 += stepsToGo1 * dirSign1
	    self.curStep2 += stepsToGo2 * dirSign2
	    print "new steps: " + str(self.curStep1) + " " + str(self.curStep2)
            import time
	    time.sleep(6)
	else:
            print "NOT RUNNING"
	

# #  myStepper1.setMaxSpeed(max1);
# #  myStepper1.setAcceleration(accel1);
# #  myStepper2.setMaxSpeed(max2);
# #  myStepper2.setAcceleration(accel2);

#        while (myStepper1.distanceToGo() * dir1 > 0) or (myStepper2.distanceToGo() * dir2 > 0):
# #    print("stepping, ");
# #    print("   , dtg:");
# #
# #    print(myStepper1.distanceToGo());
# #    print("   ");
# #    print(myStepper2.distanceToGo());
#            myStepper1.runSpeed();
#            myStepper2.runSpeed();
  


    def upRight(self, d, ratio, level, x, y):
        if (level < maxLevel):

            self.up(d,x,y);
            y = y -d;
            self.right(d,x,y);
            x = x +d;
            self.downRight(d*ratio, ratio, level + 1, x, y);
            self.upRight(d*ratio, ratio, level +1, x,y);
            self.left(d,x,y);
            x = x-d;
            self.down(d,x,y);
            y = y+d;


        return
    

    def upLeft(self, d, ratio, level, x, y):
        if (level < maxLevel):

             self.up(d,x,y);
             y=y-d;
             self.left(d,x,y);
             x=x-d;
             self.downLeft(d*ratio, ratio, level + 1,x,y);
             self.upLeft(d*ratio, ratio, level +1,x,y);
             self.right(d,x,y);
             x=x+d;
             self.down(d, x,y);
             y=y+d;


        return


    def downLeft(self, d, ratio, level,x, y):
        self.upRight(-d, ratio, level,x,y); 
        return
    

    def downRight(self, d, ratio, level, x, y):
        self.upLeft(-d, ratio, level,x,y); 
        return
    

    def up(self, d,x, y):

        self.goToXY(x,y-1.6*d);
        return
    

    def right(self, d,x, y):

      self.goToXY(x+d,y);
      return
    

    def down(self, d,x, y):
      self.up(-d,x,y);
      return
    

    def left(self, d,x, y):
      self.right(-d,x,y);
      return
    


# yo fractals yo
d = drawbot()
d.gSimple(1, 1.6, 0.4, False)




