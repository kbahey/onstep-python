#!/usr/bin/env python3
'''
Upload alignment data
'''

import time
from datetime import datetime

def batch_align():

  align = config.scope.get_align_status()
  print('Align status: ' + align)

  print('Uploading alignment points')
  # Start align
  config.scope.send_str(':SX09,0#')

  # Upload the alignment points
  # 1
  config.scope.send_str(':SX0A,03:30:37#')
  config.scope.send_str(':SX0B,60:00:13#')
  config.scope.send_str(':SX0C,03:30:34#')
  config.scope.send_str(':SX0D,60:00:04#')
  config.scope.send_str(':SX0E,-1#')
  # 2
  config.scope.send_str(':SX0A,03:06:19#')
  config.scope.send_str(':SX0B,53:30:34#')
  config.scope.send_str(':SX0C,03:06:16#')
  config.scope.send_str(':SX0D,53:30:22#')
  config.scope.send_str(':SX0E,-1#')
  # 3
  config.scope.send_str(':SX0A,03:25:41#')
  config.scope.send_str(':SX0B,49:55:34#')
  config.scope.send_str(':SX0C,03:25:38#')
  config.scope.send_str(':SX0D,49:55:24#')
  config.scope.send_str(':SX0E,-1#')
  # 4
  config.scope.send_str(':SX0A,03:10:56#')
  config.scope.send_str(':SX0B,40:57:46#')
  config.scope.send_str(':SX0C,03:10:54#')
  config.scope.send_str(':SX0D,40:57:34#')
  config.scope.send_str(':SX0E,-1#')
  # 5
  config.scope.send_str(':SX0A,03:59:08#')
  config.scope.send_str(':SX0B,40:03:45#')
  config.scope.send_str(':SX0C,03:59:06#')
  config.scope.send_str(':SX0D,40:03:35#')
  config.scope.send_str(':SX0E,-1#')
  # 6
  config.scope.send_str(':SX0A,03:55:19#')
  config.scope.send_str(':SX0B,31:56:14#')
  config.scope.send_str(':SX0C,03:55:17#')
  config.scope.send_str(':SX0D,31:56:04#')
  config.scope.send_str(':SX0E,-1#')
  # 7
  config.scope.send_str(':SX0A,03:47:27#')
  config.scope.send_str(':SX0B,24:00:17#')
  config.scope.send_str(':SX0C,03:47:25#')
  config.scope.send_str(':SX0D,24:00:06#')
  config.scope.send_str(':SX0E,-1#')
  # 8
  config.scope.send_str(':SX0A,04:58:14#')
  config.scope.send_str(':SX0B,33:11:19#')
  config.scope.send_str(':SX0C,04:58:12#')
  config.scope.send_str(':SX0D,33:11:31#')
  config.scope.send_str(':SX0E,-1#')
  # 9
  config.scope.send_str(':SX0A,06:00:56#')
  config.scope.send_str(':SX0B,44:56:52#')
  config.scope.send_str(':SX0C,06:00:54#')
  config.scope.send_str(':SX0D,44:56:53#')
  config.scope.send_str(':SX0E,-1#')
  
  print('Triggering align')
  # Trigger align
  config.scope.send_str(':SX09,1#')

  print('Align status: ' + str(config.scope.get_align_status()))
  
  count = 0
  while count < 30:
    ra = config.scope.get_ra()
    de = config.scope.get_de()
  
    cor_azm = config.scope.get_cor_azm()
    cor_alt = config.scope.get_cor_alt()
    cor_do  = config.scope.get_cor_do()

    dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print('%s - %s %s - %s %s %s' % (dt, ra, de, cor_azm, cor_alt, cor_do))

    if cor_azm != '':
      if int(cor_azm) > 0 or int(cor_azm) < 0:
        break

    count = count + 1
    time.sleep(5)

  print('Align status: ' + str(config.scope.get_align_status()))
