#!/usr/bin/env python3
'''
'''

import sys
import os
sys.path.append(os.getcwd())

import config

import init
import home
import align
import slew
import report
import backlash
import batch_align
import polar_align
import stress_test
import drift_test

menu = [
    (init.init,               'Initialize - sets Coordinates, UTC offset, Date/Time'),
    (home.home,               'Return Home'),
    (align.align,             '1 Star Align'),
    (slew.slew,               'Slew to a star'),
    (report.report,           'Report status'),
    (backlash.backlash,       'Tune Backlash'),
    (polar_align.polar_align, 'Polar Align - uses the :MP command'),
    (batch_align.batch_align, 'Batch Align - upload 9 alignment points'),
    (stress_test.stress_test, 'Stress test - repeat long slews. Useful for testing driver/motor heating.'),
    (drift_test.drift_test,   'Drift Test  - Test internal drift'),
    (sys.exit,                'Exit'),
  ]

while True:

  num = 0
  for row in menu:
    num  = num + 1
    text = row[1]

    print(str(num) + '. ' + text)

  ans = input('Enter your selection -> ')

  if ans.isnumeric():
    sel = int(ans)
    if sel > 0 and sel <= num :
      func = menu[sel-1][0]
      func()
