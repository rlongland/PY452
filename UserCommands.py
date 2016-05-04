###############################################################################
##
## User Commands: These functions are called from the internal guts. 
##                This is where you should write your own loop functions
##
###############################################################################


## Some user variables
datalength = 100

## The plot rate
rate = 10 # Hz

## Toggle whether to write data
writeData = False;

## Filename
filename = 'datafile.dat'

ARDUINO_SERIAL_PORT = '/dev/ttyACM0'
SERIAL_PORT_BAUD = 115200
PERIOD_ms = 100
PORT_TIMEOUT = 2     # seconds

##----------------------------------------------------------------------
## Setup the DAQ at the beginning
def UserSetup():
    global cr, data

    ## Setup the average time and turn on averaging for analog 0 and 1
    cr.request('!t %d' % PERIOD_ms)
    cr.request('!ai:watch 0 1')
    cr.request('!ai:watch 1 1')

    ## reset the timer
    cr.request('!resetTime')

    ## Print some diagnostics
    print 'Measurement rate = ' + cr.request('?rate')
    print 'Averaging period = ' + cr.request('?t') + ' ms'


##----------------------------------------------------------------------
def UserReadOnLoop():
    global data, ptr

    ## Grab the time
    time = float(cr.request('?time'))

    ## Grab mean readings from channel 0  and channel 1
    ch0 = float(cr.request('?ai:mean 0'))
    ch1 = float(cr.request('?ai:mean 1'))

    ## Load up the data matrix. ptr is used internally by 452DAQ to
    ## keep track of the current position in the matrix
    data[ptr,0:3] = [time,ch0,ch1]

##----------------------------------------------------------------------
def UserWriteOnLoop():
    global outputV

    incrementV = 0.1  # V
    outputV = outputV+incrementV


##----------------------------------------------------------------------
def UserStartButton():
    ## Print something
    print 'The user start functions are being run'

def UserStopButton():
    ## Print something
    print 'The user stop functions are being run'

