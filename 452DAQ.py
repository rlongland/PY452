#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Various methods of drawing scrolling plots.
"""
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.console
import numpy as np
import serial
import time
import math

## Global parameters
t0 = 0
paused = False

######################################################################
## Everything under here is the guts. You're allowed to mess with it,
## though!
execfile('UserCommands.py')  ## User-defined commands
execfile('GUI.py')           ## GUI functions
execfile('cmd.py')           ## The command-response functions

#fil = file(filename,'w')
#fil.close()
fil = None


######################################################################
## Functions to run when the buttons are pressed

# The start button
def startButton():
    global writeData, fil
    writeData=True
    # open file
    fil = open(filename, 'w')
    print 'file ' + filename + ' is open for writing!'
    ## Any additional user commands to run when "record" is pressed
    UserStartButton()

# the stop button
def stopButton():
    global writeData, fil
    writeData=False
    #close file
    fil.close()
    print 'file ' + filename + ' is closed!'
    ## Any additional user commands to run when "stop" is pressed
    UserStopButton()

# The pause button
tp=0
tr=0
def pauseButton():
    global paused, t0, tp, tr

    if paused:
        paused=False
        timer.blockSignals(False)
        tr = float(cr.request('?time'))/1e6
        t0 = t0+(tr-tp)
    else:
        paused=True
        timer.blockSignals(True)
        tp=float(cr.request('?time'))/1e6

def secretButton():
    global paused, t0, tp, tr

    if paused:
        paused=False
        timer.blockSignals(False)
        tr = float(cr.request('?time'))/1e6
        t0 = t0+(tr-tp)
        print "Finished secret signal!"
        cr.request('!secret')
    else:
        paused=True
        timer.blockSignals(True)
        tp=float(cr.request('?time'))/1e6
        print "Outputting a secret signal!"
        ## call the secret signal on the arduino
        cr.request('!secret')
        
        
def singlemeausurementButton():
    global writeData, fil

    #timer.blockSignals(True)
    writeData=True

    # open the file
    fil = open(filename, 'w')
    print 'file ' + filename + ' is open for writing!'

    ## Any additional user commands to run when "record" is pressed
    UserSingleMeasurementInit()
    #UserSingleMeasurementLoop()

def singlemeasurementStop():
    # Stop writing
    writeData=False
    #close file
    fil.close()
    print 'file ' + filename + ' is closed!'

    #timer.blockSignals(False)


# 1) Simplest approach -- update data in the array such that plot appears to scroll
#    The array size is fixed.

# Zero the data array
data = np.zeros([datalength+1, 7])
# The time array (in s)
times = 1.0/rate*np.arange(0,datalength+1,1)


# Set up the plots
# Use automatic downsampling and clipping to reduce the drawing load
pw1.setDownsampling(mode='peak')
pw1.setClipToView(True)
#pw1.setRange(xRange=[0,times[datalength]*1.5]) 
pw1.setRange(xRange=[0,datalength]) 
pw1.setLimits(xMin=0,xMax=datalength) # can't look into the past!
pw1.setLabel('left', "Y Axis")
pw1.setLabel('bottom', "Index")
pw2.setDownsampling(mode='peak')
pw2.setClipToView(True)
pw2.setRange(xRange=[0,datalength]) 
pw2.setLimits(xMin=0,xMax=datalength) # can't look into the past!
pw2.setLabel('left', "Y Axis")
pw2.setLabel('bottom', "Index")

## The lines in the plot. Preplot the zeros here and then update as
## the data arrives
curve = pw1.plot(x=times,y=data[:,1])
curve2 = pw2.plot(x=times,y=data[:,2],pen=(255,0,0))

## Open the serial port
cr = Cmd_Response(ARDUINO_SERIAL_PORT, SERIAL_PORT_BAUD)
time.sleep(2.5)
print cr.receive()

## Call the user setup routine
UserSetup()

ptr = 0
## The update function. This function gets called every time the Qt
## timer sends a signal or we can call it outselves to update the
## plots
def update():
    global data, curve, curve2, ptr

    ## if we haven't yet filled the array, increment the pointer
    if ptr < datalength:
        ptr += 1
    else:
        # once filled, slide the data left and write to the end
        data=np.roll(data,-1,axis=0)
        #pw1.autoRange()
        #pw2.autoRange()

    ## Write output voltage to Teensy
    UserWriteOnLoop()

    ## Read data from the arduino using the user-defined read function
    UserReadOnLoop()
        
    #----------------------------------------------------------------------
    # PY452
    # HERE is where you can edit the read data. Conversions to
    # current, voltage, etc. are performed on the data arrays. 
    # 
    # Write to file here, also!
    if not fil is None:
        if not fil.closed: 
#            fil.write(',\t'.join(map(repr, data[ptr,:])) + '\n')
            fil.write(',\t'.join('{1:.4}'.format(*k) for k in enumerate(data[ptr,:])) + '\n')

    # Set the graph data. Note that we write from right to left, so
    # the time array counts backwards!
    i = np.arange(0,ptr,1)
    #curve.setData(x=data[:ptr,0],y=data[:ptr,1])
    curve.setData(x=i,y=data[:ptr,1])
    #    curve2.setData(x=data[:ptr,0],y=data[:ptr,2])
    curve2.setData(x=i,y=data[:ptr,2])
            

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

