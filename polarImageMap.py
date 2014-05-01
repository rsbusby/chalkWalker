



## methods for determining whether chalkwalker should drop chalk at the given location

from time import sleep

from PIL import Image

from math import sqrt, atan, pi, atan2, sin, cos


def test(r,theta):

    if r < 27:
        return True




    return False


from bisect import bisect_left

def takeClosest(myList, myNumber):
    """
    Assumes myList is sorted. Returns closest value to myNumber.

    If two numbers are equally close, return the smallest number.
    """
    pos = bisect_left(myList, myNumber)

    #print "pos: " + str(pos)
    
    if pos == 0:
        return myList[0]
    if pos == len(myList):
        return myList[-1]
    before = myList[pos - 1]
    after = myList[pos]
    if after - myNumber < myNumber - before:
       return after
    else:
       return before


class polarImageMap(object):


    
    def init(self, filename):
        ## given a monochrome image, map to polar coords, kept in memory so don't go crazy w/ size
        myimage = Image.open(filename)
        sz = myimage.size
        self.sz = sz
        self.d = myimage.getdata()

    def initOld(self, filename):
        ## given a monochrome image, map to polar coords, kept in memory so don't go crazy w/ size
        myimage = Image.open(filename)
        sz = myimage.size
        self.sz = sz
        d = myimage.getdata()
        for i in range(0, sz[1]): 
            pp = d.getpixel((sz[0]/2, i))
            #if pp < 10:
            #    print("Pixel " + str(i) + " is dark")


        ## ok, let's map to polar coords
        i2 = myimage.copy()
        r = []
        t = []

        import numpy
        r = numpy.zeros(sz[0])
        t = numpy.zeros(sz[1])
        f = numpy.zeros((sz[0], sz[1]))


        ##ind = 0
        
        for i in range(0, sz[0]): 
            for j in range(0, sz[1]): 


                x = i - (sz[0] / 2)
                y = sz[1] / 2 - j
                ##print str(x) + " " + str(y)
                radius = sqrt(x*x + y*y)
                theta = atan2(float(y), float(x))
                pp = d.getpixel((i,j))
                #r[ind] = radius
                #t[ind] = theta
                #ind = ind + 1
                if pp < 10:
                    print("YEP:  ", radius, "  " , theta, "      ", pp , "   x: ", str(x), ", y: ",str(y), "  ",str(sz[0])," ",str(sz[1]))
                    # sleep(0.5)
                    f[i][j] = 1
                ##else:
                    ##print(radius, "  " , theta)

        for i in range(0, sz[0]): 
            x = i - (sz[0] / 2)
            radius = sqrt(x*x + y*y)
            r[i] = radius

        for j in range(0, sz[1]): 
            y = sz[1] / 2 - j
            theta = atan2(float(y), float(x))
            t[j] = theta

            
        self.r = r
        self.theta = t
        self.f = f


        print str(r[0])  + "  " + str(r[-1])
        print str(t[0])  + "  " + str(t[-1])        

    def polarToCart(self, radius, theta):
        ## given r, theta, is the image at the corresponding x,y coordinates above threshold?

        ## x = r cos theta
        ## 0 -> s/2, s/2 -> s
        ## y = r sin theta
        ## 
        x = radius * cos(theta) 
        y = radius * sin(theta)

        xInt = int(x) + self.sz[0] / 2
        yInt = int(y) + self.sz[1] / 2
        
        try:
            pp = self.d.getpixel((xInt,yInt))
            if pp < 10:
                 return True

        except:
            pass

        return False

        

    def query(self,radius,theta):

        ## return boolean, whether image is above threshold at that coordinate.
        ## cool (slow)trick to find closest index is from StackOverflow
        thetaMod = theta % pi  - pi
        rInd = min(range(len(self.r)), key=lambda i: abs(self.r[i]-radius))
        tInd = min(range(len(self.theta)), key=lambda i: abs(self.theta[i]-thetaMod))


        ## would work if they were sorted....
        #rInd = takeClosest(self.r, radius)
        #tInd = takeClosest(self.theta, thetaMod)

        
        
        
        val = self.f[rInd][tInd]

        print str(radius) + " " + str(rInd) + ": " + str(self.r[rInd]) + "    " + str(thetaMod) + " " + str(tInd) + ": " + str(self.theta[tInd]) + "  closest   "  + str(val)
        
        if val == 1:
            print "YYYYAAAY"
            return True
        
        return False
    
        
