#!/usr/bin/env python3
'''
Testing of drift by a given controller, by reporting angular coordinates
'''

import time
from datetime import datetime
import config

# Calculate the drift in RA

def drift_test(iterations = 60, interval = 10):
  ra_min = 0.0
  count = 0

  while True:
    # Increment the iteration counter
    count = count + 1
    # Check if we reached the maximum count, and exit
    if count > iterations:
      time.sleep(3)
      return

    curr_ra = config.scope.get_ra()
    curr_de = config.scope.get_de()

    home = '    '
    if config.scope.is_home is True:
      home = 'Home'

    status = 'N/A'
    if config.scope.is_slewing is True:
      status = 'SLW'

    if config.scope.is_tracking is True:
      status = 'TRK'

    equ  = config.scope.get_debug_equ()
    ra = float(equ.split(',')[0])
    de = float(equ.split(',')[1])
    if ra_min == 0.0:
      # First pass, initialize values
      ra_min = ra
      ra_max = ra
      de_min = de
      de_max = de
      time_start = datetime.now()
      ra_arc_secs = 0.0
      de_arc_secs = 0.0

    else:
      # Record maximums and minimums
      if ra < ra_min:
        ra_min = ra
      if ra > ra_max:
        ra_max = ra

      if de < de_min:
        de_min = de
      if de > de_max:
        de_max = de

      # Calculate elapsed time
      time_now = datetime.now()
      elapsed = (time_now - time_start)
      secs = elapsed.seconds

      # calculate drift
      ra_arc_secs = ((ra_max - ra_min) / 0.000278) / (secs / 60)
      de_arc_secs = ((de_max - de_min) / 0.000278) / (secs / 60)

    dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print('%s %s %s %s %s %s %s %s' % (dt, home, status, curr_ra, curr_de, equ, '{:6.3f}'.format(ra_arc_secs), '{:6.3f}'.format(de_arc_secs)))
    
    try:
      time.sleep(interval)
    except KeyboardInterrupt:
      print('Exiting ...')
      time.sleep(3)
      return

