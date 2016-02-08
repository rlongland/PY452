# -*- coding: utf-8 -*-
"""
Various methods of drawing scrolling plots.
"""
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.console
import numpy as np
import serial

## Use serial port?
useSerial = False

## Some user variables
datalength = 1000

## The plot rate
rate = 100 # Hz

## Toggle whether to write data
writeData = False;

## Filename
filename = 'datafile.dat'

######################################################################
## Functions to run when the buttons are pressed

# The start button
def startButton():
    global writeData, fil
    writeData=True
    # open file
    #with open(filename, 'w') as fil
    fil = open(filename, 'w')
    print 'file ' + filename + ' is open for writing!'

# the stop button
def stopButton():
    global writeData, fil
    writeData=False
    #close file
    fil.close()
    print 'file ' + filename + ' is closed!'

######################################################################
## Everything under here is the guts. You're allowed to mess with it,
## though!
execfile('GUI.py')

#fil = file(filename,'w')
#fil.close()
fil = None

# 1) Simplest approach -- update data in the array such that plot appears to scroll
#    The array size is fixed.

# Zero the data array
data = np.zeros([datalength+1, 5])
# The time array (in s)
time = -1.0/rate*np.arange(datalength+1,0,-1)


#p = pw.addPlot()
# Set up the plot
# Use automatic downsampling and clipping to reduce the drawing load
pw.setDownsampling(mode='peak')
pw.setClipToView(True)
pw.setRange(xRange=[time[0], 0])  # Time is all in the past (time[0] is -10 seconds, for eg)
pw.setLimits(xMax=0) # can't look into the future!
pw.setLabel('left', "Y Axis")
pw.setLabel('bottom', "Time", units="s")

## The lines in the plot. Preplot the zeros here and then update as
## the data arrives
curve = pw.plot(x=time,y=data[:,1])
curve2 = pw.plot(x=time,y=data[:,2],pen=(255,0,0))

## Open the serial port
if useSerial:
    raw=serial.Serial("/dev/ttyACM0",9600)
    raw.open()

ptr = 0
## The update function. This function gets called every time the Qt timer sends a signal
def update():
    global data, curve, curve2, ptr

    ## if we haven't yet filled the array, increment the pointer
    if ptr < datalength:
        ptr += 1
    else:
        # once filled, slide the data left and write to the end
        data=np.roll(data,-1,axis=0)

    ## Read the serial data
    if useSerial:
        line = raw.readline()
        data[ptr,:] = [float(val) for val in line.split()]
        #data[ptr,0] = float(line)
    else:
        # or just generate some random numbers
        data[ptr,0:2] = [np.random.normal(), np.random.normal()]
        
        #----------------------------------------------------------------------
        # PY452
        # HERE is where you can edit the read data. Conversions to
        # current, voltage, etc. are performed on the data arrays. 
        # 
        # Write to file here, also!
        if not fil is None:
            if not fil.closed: 
                fil.write(', '.join(map(repr, data[ptr,:])) + '\n')

        # Set the graph data. Note that we write from right to left, so
        # the time array counts backwards!
        curve.setData(x=time[-ptr:],y=data[:ptr,0])
        curve2.setData(x=time[-ptr:],y=data[:ptr,1])
            

## Update the plots using Qt
## Update rate is used to determine the delay
timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(1000/rate)  ## in miliseconds

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()

