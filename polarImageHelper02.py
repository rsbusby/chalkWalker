from time import sleep

import socket               # Import socket module
import random

import math

import polarImageMap

## client stuff
sc = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
cport = 5204                # Reserve a port for your service.
#sc.close()   


## server stuff
s = socket.socket()         # Create a socket object
#host = socket.gethostname() # Get local machine name
port = 10002                # Reserve a port for your service.
#s.close()
s.bind((host, port))        # Bind to the port

s.listen(50)                 # Now wait for client connection.
i = 9
c, addr = s.accept()     # Establish connection with client.
print 'Got connection from', addr


sc.connect((host, cport))

c.send("N")

## set up image mapping

pim = polarImageMap.polarImageMap()

pim.init("new.pbm")

while True:


   i = i+ 1
   #c.send(str(i))
   #c.close()                # Close the connection
     

   #while True:

   fromPlotter = sc.recv(1024)
   #sc.close       

   polarPlotCoords = fromPlotter.split(' ')
   r = float(polarPlotCoords[0])
   theta = float(polarPlotCoords[1]) 

   ##print str(r) + "   " + str(theta) + "  " + str(theta % math.pi)

   # plotFlag = pim.query(r, theta)
   plotFlag = pim.polarToCart(r, theta)

   if not plotFlag: 
       c.send("Y")   
   else:
       c.send("N") 
