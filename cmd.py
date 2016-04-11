## cmd_response wrapper for python

class Cmd_Response(object):
  '''interface class with cmd_response Arduino sketch'''

  def __init__(self, serial_port, baud=115200, 
               delimiter='\n', timeout=PORT_TIMEOUT):
    self.serial_port = serial_port
    self.baud = baud
    self.delimiter = delimiter
    self.timeout = timeout
    self.port = serial.Serial(serial_port, baud, timeout=self.timeout)
    self.port.flushInput()

  def send(self, cmd):
    '''write the command to the USB port'''
    self.port.write(cmd + self.delimiter)

  def receive(self):
    '''read the device response from the USB port'''
    return self.port.readline().strip()
  
  def request(self, cmd):
    '''return the result from the command'''
    self.send(cmd)
    return self.receive()
  
  def report(self, cmd):
    '''print the response to the command'''
    print "%s  " % cmd,
    print self.request(cmd)
