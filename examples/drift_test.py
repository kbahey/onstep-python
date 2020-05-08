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

  print('Time            OnStep Time   Sidereal      St  RA       DE        Equ                  RA"/min RA"Max DE"/min DE"Max')

  while True:
    # Increment the iteration counter
    count = count + 1
    # Check if we reached the maximum count, and exit
    if count > iterations:
      time.sleep(1)
      return

    curr_ra = config.scope.get_ra()
    curr_de = config.scope.get_de()

    local_tm    = config.scope.get_time(True)
    sidereal_tm = config.scope.get_sidereal_time(True)
    dt          = datetime.now().strftime('%H:%M:%S.%f')

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
      ra_max_drift = 0.0
      de_max_drift = 0.0
      ra_drift = 0.0
      de_drift = 0.0
      ra_avg = 0.0
      de_avg = 0.0

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
      ra_drift = (ra_max - ra_min) / 0.000278
      de_drift = (de_max - de_min) / 0.000278

      ra_arc_secs = ra_drift / (secs / 60)
      de_arc_secs = de_drift / (secs / 60)

    # format results
    ra_avg = '{:6.3f}'.format(ra_arc_secs)
    de_avg = '{:6.3f}'.format(de_arc_secs)

    ra_max_drift = '{:6.3f}'.format(ra_drift)
    de_max_drift = '{:6.3f}'.format(de_drift)

    print('%s %s %s %s %s %s %s %s %s %s %s' % (dt, local_tm, sidereal_tm, status, curr_ra, curr_de, equ, ra_avg, ra_max_drift, de_avg, de_max_drift))
    
    try:
      time.sleep(interval)
    except KeyboardInterrupt:
      print('Exiting ...')
      time.sleep(1)
      return
