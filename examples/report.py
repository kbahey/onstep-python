#!/usr/bin/env python3
'''
Report on the status of the teleconfig.scope
'''

import time
from datetime import datetime
import config

def report(interval = 10):

  while True:
    curr_ra = config.scope.get_ra()
    curr_de = config.scope.get_de()

    status = '---'

    if config.scope.is_slewing is True:
      status = 'SLW'
      
    if config.scope.is_tracking is True:
      status = 'TRK'

    if config.scope.is_home is True:
      status = 'HOM'

    dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print('%s %s %s %s' % (dt, status, curr_ra, curr_de))
    
    try:
      time.sleep(interval)
    except KeyboardInterrupt:
      print('Exiting ...')
      time.sleep(3)
      return

