"""
Polar Helper.

Usage:
  polarImageHelperArd.py <image> ... [options]
  polarImageHelperArd.py -h | --help
  polarImageHelperArd.py --version
  polarImageHelperArd.py
  

Options:
  -h --help     Show this screen.
  --version     Show version.
  <image>  Image file, in any format that ImageMagick accepts
  --drifting    Drifting mine
  --using-processing  using Processing over client/server instead of Arduino over serial [default: False]  

"""

from time import sleep

import socket               # Import socket module
import random

import math

import polarImageMap
import commands

import sys

from docopt import docopt




arguments = docopt(__doc__, version='Polar Helper Version 1.3')
print(arguments)
print(arguments['<image>'])

usingProcessing = False
if arguments['--using-processing']:
  usingProcessing = True

print "UP "
print usingProcessing
##sys.exit()

import serial

## Some previous USB ports
## serial.tools.list_ports will print a list of available ports
s1 = "/dev/tty.usbserial-A600ailE"
s2 = "/dev/tty.usbmodem12341"
if not usingProcessing:
    ser = serial.Serial(s1, 9600) # Establish the connection on a specific port
    write_to_comm = ser.write
else:
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
    write_to_comm = c.send
    write_to_comm("N")

print "set up image"
## set up image

# im = "new.pbm"

imOrig = arguments['<image>'][0]
im = "test.pbm"
commands.getoutput("convert " + imOrig + " -resize 400x400 " + "temp.png")

imTmp = "temp.png"

commands.getoutput("convert " + imTmp + " -colorspace gray -threshold 35% " + im )

print "DB 3"

## set up image mapping
pim = polarImageMap.polarImageMap()
pim.init(im)

count = 0
## loop forever

print "DB 6"

if usingProcessing:
    #fromPlotter = sc.recv(1024)
    a = 9
else:
    fromPlotter = ser.readline()

    print "from: " + fromPlotter

    if fromPlotter.count("Ready") < 1:
      print "WTF"
      sys.exit()
    else:
      ser.write("OK")

while True:

    ## get info from plotter
    if usingProcessing:
        fromPlotter = sc.recv(1024)
    else:
        fromPlotter = ser.readline()

    print "from "
    print fromPlotter
    polarPlotCoords = fromPlotter.split(' ')
    r = float(polarPlotCoords[0])
    theta = float(polarPlotCoords[1]) 

    print str(r) + "   " + str(theta) + "  " + str(theta % math.pi)

    plotFlag = pim.polarToCart(r, theta)

    if not plotFlag: 
        #c.send("Y")   
        write_to_comm("Y")



    else:
        #c.send("N") 
        write_to_comm("N")

    count = count + 1
    print count
    #sleep(1) # Delay

##sc.close()           
## c.close()
