#!/usr/bin/env python3
'''
Report on the status of the teleconfig.scope
'''

import time
from datetime import datetime
import config

def report(interval = 10):

  # Display date, time, UTC offset, and latitude/longitude
  dt  = config.scope.get_date()
  tm  = config.scope.get_time()
  ut  = config.scope.get_utc()
  lt  = config.scope.get_latitude()
  lg  = config.scope.get_longitude()
  lst = config.scope.get_sidereal_time()
  print('Date: %s Time: %s UTC %s Lat: %s Long: %s LST: %s' % (dt, tm, ut, lt, lg, lst))

  print('Time     Stat Mnt-Time RA       DEC       Alt       Azm      ')
  while True:

    scope_tm = config.scope.get_time()
    dt = datetime.now().strftime('%H:%M:%S')

    curr_ra = config.scope.get_ra()
    curr_de = config.scope.get_de()
    curr_alt = config.scope.get_alt()
    curr_azm = config.scope.get_azm()

    status = '---'
    if config.scope.is_slewing is True:
      status = 'SLW'
      
    if config.scope.is_tracking is True:
      status = 'TRK'

    if config.scope.is_home is True:
      status = 'HOM'

    print('%s %s  %s %s %s %s %s' % (dt, status, scope_tm, curr_ra, curr_de, curr_alt, curr_azm))
    
    try:
      time.sleep(interval)
    except KeyboardInterrupt:
      print('Exiting ...')
      time.sleep(1)
      return

