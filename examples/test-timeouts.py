#!/usr/bin/env python3

# This is an example of a simple script that can measure 
# timeouts and compare 'over USB' to 'over WiFi'

# Specify the mode, either 'wifi' or 'usb'
mode = 'wifi'

# This applies when you are over WiFi
HOST_WIFI = '192.168.0.212'
PORT_WIFI = '9997'

# And these when you are over USB
HOST_USB = ''
PORT_USB = '/dev/ttyUSB0' # Some boards require /dev/ttyACM0

# Do not change anything below that line
import sys
import time
import os
sys.path.append(os.getcwd())

import lx200.onstep as onstep

# Create a scope object
if mode == 'wifi':
  HOST = HOST_WIFI
  PORT = PORT_WIFI
else:
  HOST = HOST_USB
  PORT = PORT_USB
  
scope = onstep.onstep(host = HOST, port = PORT)

# Execute commands
for cmd in ('GD', 'GR', 'rG','rI','rM','rT','rb','FA','FG','FT','FM','FI'):
  start = time.time()
  r = scope.send_str(':' + cmd + '#')
  end = time.time()
  print('%2.3f %s %s' % (end - start,cmd, r))
  time.sleep(0.01)

