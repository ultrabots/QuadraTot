import math, pdb, sys
import random
import os
import string
from datetime import datetime
from copy import copy
from time import sleep
from RobotConstants import MIN_INNER, MAX_INNER, MIN_OUTER, MAX_OUTER, MIN_CENTER, MAX_CENTER, NORM_CENTER

class simrun:
    ''' simulation running '''

    def __init__(self):
        self.filename = "output.txt"
 
    def runSim(self, gaitFunction):

        os.remove('/home/sean/quadratot/code/input.txt')
        
        ff = file('input.txt', "w")
        timeMax = 12.0
        timeDiv = 1.0/60.0
        divs = int(timeMax/timeDiv)
        t = 0.0

        for i in xrange(0,divs):
            gait = gaitFunction[0](t)
            length = len(gait)
            t = t+timeDiv
            if t == timeMax:
                ff.write(str(t) + ' ')

                for ii in xrange(0, length):
                    ff.write(str(gait[ii]) + ' ')

            else:
                ff.write(str(t) + ' ')
                for ii in xrange(0,length):
                    ff.write(str(gait[ii]) + ' ')
                ff.write('\n')
                           
        ff.close()    
        os.system('./crossSim -i input.txt -o output.txt -n')
        dist = self.getDist()      
        return dist
    
    def getDist(self):

        outputRaw= file(self.filename,"r")
        outputData = [line.split() for line in outputRaw]
        outputColLen = len(outputData)-1
        outputRowLen = len(outputData[1])-1
        posBeg = [outputData[1][outputRowLen-2], outputData[1][outputRowLen-1], outputData[1][outputRowLen]]
        posEnd = [outputData[outputColLen][outputRowLen-2], outputData[outputColLen][outputRowLen-1], outputData[outputColLen][outputRowLen]]

        # finds the distance the robot travelled using x and y '
        xdist = float(posEnd[0])-float(posBeg[0])
        zdist = float(posEnd[2])-float(posBeg[2])
#        zdist = float(self.posEnd[2])-float(self.posBeg[2])
        return math.sqrt(math.pow(xdist,2)+math.pow(zdist,2))

    def cropPosition(self, position, cropWarning = False):
        # crops the given positions to their apropriate min/max values.
        #Requires a vector of length 9 to be sure the IDs are in the assumed order.'''
        ret = copy(position)
        for ii in [0, 2, 4, 6]:
            ret[ii] = max(MIN_INNER, min(MAX_INNER, ret[ii]))
            ret[ii+1] = max(MIN_OUTER, min(MAX_OUTER, ret[ii+1]))
        ret[8] = max(MIN_CENTER, min(MAX_CENTER, ret[8]))

        if cropWarning and ret != position:
            print 'Warning: cropped %s to %s' % (repr(position), repr(ret))

        return ret

    
