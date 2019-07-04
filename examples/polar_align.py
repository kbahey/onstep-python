#!/usr/bin/env python3
'''
This is a program to refine the polar alignment
'''

import time
import config

p1 = '''
This procedure will help get the mount polar aligned:

1. Do a rough alignment using the polar scope.
2. Start KStars, connect INDI, and change Align to "Sync".
3. Using Mount Model in KStars, do a 3 star (or more) Align.
4. From INDI's align tab, record the polar align errors.
5. Choose a bright star in KStars.
6. In the Align Tab, change Align to "Slew to Target", then click "Capture"
7. If necessary, change the speed to 1X, and use the hand controller to perfectly center the star.
8. If you did, then Sync again, from KStars.
9. Disconnect INDI in KStars.

Hit ENTER when you have done all the above: '''

p2 = '''
10. Using ONLY the Alt and Azimuth controls, center the star perfectly.

Hit ENTER when ready: '''

p3 = '''
11. The mount will now return to the home position
12. Repeat the 3-star align procedure

Hit ENTER to return to the home position: '''

def polar_align():
  # Display first prompt
  ans = input(p1)

  print('Slewing to assumed position')
  if config.scope.slew_polar() == False:
    print('Slew to assumed position failed')
    time.sleep(3)
    return

  # Center the star using Alt and Az only
  ans = input(p2)

  # Return home
  ans = input(p3)

  if config.scope.return_home() == False:
    print('Return Home command failed')
    time.sleep(3)
    return

  print('Returning to home position')
