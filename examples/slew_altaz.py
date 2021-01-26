#!/usr/bin/env python3
'''
This is the program used to end a test sequence. 
It displays the date/time, UTC offset, latitude and longitude
It then issues the command to return the config.scope to the home position
'''

import time
import config

def slew_altaz():

  rc = config.scope.tracking_on()
  if rc == '0':
    print('Error turning tracking on: ', rc)

  rc = config.scope.set_target_alt(config.alt)
  if rc == '0':
    print('Error setting target Alt: ', rc)

  rc = config.scope.set_target_azm(config.azm)
  if rc == '0':
    print('Error setting target Azm: ', rc)

  print('Slewing to %s %s' % (config.alt, config.azm))
  rc, msg = config.scope.slew_hor()
  if rc != '0':
    print('Slew failed: rc: ' + str(rc) + ', ' + msg)
    time.sleep(1)
    return

