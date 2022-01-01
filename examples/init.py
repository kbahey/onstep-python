#!/usr/bin/env python3
'''
Start of session initialization

Sets the following parameters:

- date (from computer running this program)
- time (from computer running this program)
- UTC offset (from config.py config file)
- Latitude (from config.py config file)
- Longitude (from config.py config file)
- Horizon/Overhead limits (from config.py config file)

Then, turns on tracking
'''

import time
from datetime import datetime
import config

WAIT_SECONDS = 0.3
def init():

  ver = config.scope.get_version()
  print('OnStep Version: %s' % (ver))

  if config.lat == '' or config.lon == '':
    print('Please change config.py to add lat and lon parameters')
    time.sleep(WAIT_SECONDS)
    return

  # Set the basic parameters
  if config.scope.set_date() == False:
    print('Set date failed')
    time.sleep(WAIT_SECONDS)
    return

  if config.scope.set_time() == False:
    print('Set time failed')
    time.sleep(WAIT_SECONDS)
    return

  if config.scope.set_utc_offset(config.utc) == False:
    print('Set UTC Offset failed')
    time.sleep(WAIT_SECONDS)
    return

  if config.scope.set_latitude(config.lat) == False:
    print('Set latitude failed')
    time.sleep(WAIT_SECONDS)
    return

  if config.scope.set_longitude(config.lon) == False:
    print('Set longitude failed')
    time.sleep(WAIT_SECONDS)
    return

  if config.scope.set_horizon_limit(config.hor_lim) == False:
    print('Set horizon limit failed')
    time.sleep(WAIT_SECONDS)
    return

  if config.scope.set_overhead_limit(config.ovh_lim) == False:
    print('Set overhead limit failed')
    time.sleep(WAIT_SECONDS)
    return

  # Display date, time, UTC offset, and latitude/longitude
  dt = config.scope.get_date()
  tm = config.scope.get_time()
  ut = config.scope.get_utc()
  lt = config.scope.get_latitude()
  lg = config.scope.get_longitude()
  print('Date: %s Time: %s UTC %s Lat: %s Long: %s' % (dt, tm, ut, lt, lg))

  print('Starting tracking')
  if config.scope.tracking_on() == '0':
    print('Tracking failed')
    time.sleep(WAIT_SECONDS)
    return

