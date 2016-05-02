###############################################################################
##
## User Commands: These functions are called from the internal guts. 
##                This is where you should write your own loop functions
##
###############################################################################

def UserReadOnLoop():

    ## Grab the time
    time = float(cr.request('?time'))

    ## Grab mean readings from channel 0  and channel 1
    ch0 = float(cr.request('?ai:mean 0'))
    ch1 = float(cr.request('?ai:mean 1'))

