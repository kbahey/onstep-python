#!/usr/bin/env python3
'''
Do a 1 star align
'''

import os
import config

def align():

  print('Start Align')
  if config.scope.align() == '0':
    print('Align failed')
    time.sleep(3)
    return

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

