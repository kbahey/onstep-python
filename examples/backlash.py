#!/usr/bin/env python3
'''
Backlash tuning
'''
import time
import config

msg_instr_1 = '''Please do the following:
1. Slew the scope to a terrestrial object
2. Center the object carefully
3. You must end the motion with the %s button.
Hit Enter when done --> '''

msg_info = '''The scope will now move away from the object.
Hit Enter when motion is complete --> '''

msg_instr_2 = '''Now move the object back, centering it perfectly, using only the %s button.
Hit Enter when you have done so --> '''

msg_update = '''Update mount with new calculated backlash?
Enter Y to accept or anything else to ignore --> '''

msg_test = '''Now test this axis by slewing back and forth, and observing no jumps or lags.
Hit Enter when done --> '''

params = [
  ('East', 'w'),
  ('South', 'n'),
  ]

def backlash():

  print('Starting tracking')
  if config.scope.tracking_on() == '0':
    print('Tracking failed')
    time.sleep(3)
    return

  print('Stopping tracking')
  if config.scope.tracking_off() == '0':
    print('Tracking stop failed')
    time.sleep(3)
    return

  for axis in 1, 2:
    print('=====\nAxis: ' + str(axis))

    button = params[axis-1][0]
    direction = params[axis-1][1]

    # Display current backlash
    old_backlash = config.scope.get_backlash(axis)
    print('Current backlash: ' + str(old_backlash) + ' arc seconds')

    # Zero out the backlash
    print('Zeroing out backlash')
    config.scope.set_backlash(axis, 0)

    ans = input(msg_instr_1 % (button))

    # Set to low speed
    print('Setting speed to 1X')
    config.scope.set_speed('1x')

    ans = input(msg_info)
    # Get motor position before movement
    pos1 = config.scope.get_ax_motor_pos(axis)

    # Move in the set direction
    config.scope.move(direction)
    # Time for about 240 arc seconds @ 1X 15"/sec, which should be enough for the worst backlash
    time.sleep(16)
    # Stop motion
    config.scope.stop()

    ans = input(msg_instr_2 % (button))

    # Get motor position after movement
    pos2 = config.scope.get_ax_motor_pos(axis)

    # Get steps per degree
    spd = int(config.scope.get_spd(axis))

    print('pos1=%s pos2=%s spd=%s' % (str(pos1), str(pos2), str(spd)))

    # Calculate the backlash value
    steps = abs(float(pos1) - float(pos2))

    backlash = round((steps * 3600) / spd)

    print('Calculated backlash: ' + str(backlash) + ' arc seconds')

    ans = input(msg_update)
    if ans == 'Y' or ans == 'y':
      if backlash <= 999:
        print('Setting backlash to calculated value')
        config.scope.set_backlash(axis, backlash)
        ans = input(test)
      else:
        print('ERROR: backlash is more than maximum of 999')
    else:
        print('Reverting backlash to old value')
        config.scope.set_backlash(axis, old_backlash)
