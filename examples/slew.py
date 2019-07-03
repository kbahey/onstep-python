#!/usr/bin/env python3
'''
This is the program used to end a test sequence. 
It displays the date/time, UTC offset, latitude and longitude
It then issues the command to return the config.scope to the home position
'''

import time
import config

def slew():

  rc = config.scope.tracking_on()
  if rc == '0':
    print('Error turning tracking on: ', rc)

  rc = config.scope.set_target_ra(config.ra)
  if rc == '0':
    print('Error setting target RA: ', rc)

  rc = config.scope.set_target_de(config.de)
  if rc == '0':
    print('Error setting target DE: ', rc)

  print('Slewing to %s %s' % (config.ra, config.de))
  rc, msg = config.scope.slew_equ()
  if rc != '0':
    print('Slew failed: rc: ' + str(rc) + ', ' + msg)
    time.sleep(3)
    return

