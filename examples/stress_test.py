#!/usr/bin/env python3
'''
Stress test a teleconfig.scope by repeatedly doing long slews
'''
import time
from datetime import datetime
import config

# Configuration parameters
alt   = '+05:00:00'
azm_w = '190:00:00'
azm_e = '170:00:00'

num_iterations    = 25
poll_duration     = 10
tracking_duration = 5

def print_status():
  status = '---'
  curr_alt = config.scope.get_alt()
  curr_azm = config.scope.get_azm()
  dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
  if config.scope.is_slewing is True:
    status = 'SLW'
  if config.scope.is_tracking is True:
    status = 'TRK'
  if config.scope.is_home is True:
    status = 'HOM'
  print('%s %s %s %s' % (dt, status, curr_alt, curr_azm,))

def slew(target_alt, target_azm):
  config.scope.update_status()
  if config.scope.is_slewing is True:
    print('Scope already slewing')
    time.sleep(1)
    return

  rc = config.scope.set_target_azm(target_azm)
  if rc == '0':
    print('Error setting target AZ: ', rc)

  rc = config.scope.set_target_alt(target_alt)
  if rc == '0':
    print('Error setting target ALT: ', rc)

  print('Slewing to Alt:%s AZ:%s' % (target_alt, target_azm))
  rc, msg = config.scope.slew_hor()
  if rc != '0':
    print('Slew failed: rc: ' + str(rc) + ', ' + msg)
    time.sleep(1)
    return

def start_tracking():
  print('Starting tracking')
  if config.scope.tracking_on() == '0':
    print('Tracking failed')
    time.sleep(WAIT_SECONDS)
    return

def return_home():
  print('Returning to home postion')
  if config.scope.return_home() == False:
    print('Return Home command failed')
    time.sleep(1)
    return

  while True:
    config.scope.update_status()
    if config.scope.is_home is True:
      print('Successfully returned to home position')
      return

def do_test():
  count = 0

  while True:
    # Increment the iteration counter
    count = count + 1
    # Check if we reached the maximum count, and exit
    if count > num_iterations:
      print('Test completed')
      time.sleep(1)
      return

    # Start an iteration
    print('Iteration: ' + str(count))

    # Switch between east of meridian and west of it, using azimuth
    if count % 2: 
      azm = azm_w
    else:
      azm = azm_e

    # Slew to target location
    slew(alt, azm)

    slew_end = False
    # Check for end of slew
    while slew_end is False:

      try:
        # Check if the slew ended
        config.scope.update_status()
        if config.scope.is_slewing is False and config.scope.is_tracking is True:
          # Slew ended
          slew_end = True

        print_status()
        time.sleep(poll_duration)

      except KeyboardInterrupt:
        print('Exiting ...')
        time.sleep(1)
        return

    # Scope now tracking
    print_status()
    time.sleep(tracking_duration)

def stress_test():
  start_tracking()

  do_test()

  return_home()

