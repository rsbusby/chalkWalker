from time import sleep

import socket               # Import socket module
import random

import math

import polarImageMap
import commands

## set up client and server to communicate with corresponding client/server on Processing
host = socket.gethostname() # Get local machine name

## client stuff
sc = socket.socket()         # Create a socket object
cport = 5204                # Reserve a port for the client

## server stuff
s = socket.socket()         # Create a socket object
port = 10002                # Reserve a port for the service
s.bind((host, port))        # Bind to the port

s.listen(50)                 # Now wait for client connection
c, addr = s.accept()     # Establish connection with client
print 'Got connection from', addr


sc.connect((host, cport))

c.send("N")

## set up image

# im = "new.pbm"

imOrig = "test.jpg"
im = "test.pbm"
commands.getoutput("convert " + imOrig + " -resize 400x400 " + "temp.png")

imTmp = "temp.png"

commands.getoutput("convert " + imTmp + " -colorspace gray -threshold 35% " + im )

## set up image mapping
pim = polarImageMap.polarImageMap()
pim.init(im)

## loop forever
while True:

   fromPlotter = sc.recv(1024)

   polarPlotCoords = fromPlotter.split(' ')
   r = float(polarPlotCoords[0])
   theta = float(polarPlotCoords[1]) 

   ##print str(r) + "   " + str(theta) + "  " + str(theta % math.pi)

   plotFlag = pim.polarToCart(r, theta)

   if not plotFlag: 
       c.send("Y")   
   else:
       c.send("N") 


##sc.close()           
## c.close()
