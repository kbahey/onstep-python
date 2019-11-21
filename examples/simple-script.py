#!/usr/bin/env python3

# This is an example of a simple script that you can use to 
# build other more complex scripts that do complex tasks

HOST = '192.168.0.212'
PORT = '9999'

# Do not change anything below that line
import sys
import time
import os
sys.path.append(os.getcwd())

import lx200.onstep as onstep

# Create a scope object
scope = onstep.onstep(host = HOST, port = PORT)

# Execute commands
for i in range(1, 10):
  r = scope.send_str(':GU#')
  print(r)
  time.sleep(5)

