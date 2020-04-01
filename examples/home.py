#!/usr/bin/env python3
'''
This is the program used to end a test sequence.
It displays the date/time, UTC offset, latitude and longitude
It then issues the command to return the scope to the home position
'''

import time
import sys
import os
sys.path.append(os.getcwd())

import config

def home():

  print('Returning to home postion')
  if config.scope.return_home() == False:
    print('Return Home command failed')
    time.sleep(3)
    return

  while True:
    config.scope.update_status()
    if config.scope.is_home is True:
      print('Successfully returned to home position')
      return

    time.sleep(10)

