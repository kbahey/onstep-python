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
import slew_altaz
import report
import backlash
import batch_align
import polar_align
import stress_test
import drift_test

menu = [
    ('i',  init.init,                'Initialize - sets Coordinates, UTC offset, Date/Time'),
    ('h',  home.home,                'Return to Home position'),
    ('r',  report.report,            'Report mount status'),
    ('a',  align.align,              '1 Star Align'),
    ('s',  slew.slew,                'Slew to a star'),
    ('sz', slew_altaz.slew_altaz,    'Slew to Alt/Azm'),
    ('dt', drift_test.drift_test,    'Drift Test  - Test internal drift'),
    ('ba', batch_align.batch_align,  'Batch Align - upload 9 alignment points'),
    ('st', stress_test.stress_test,  'Stress test - repeat long slews. Useful for testing driver/motor heating.'),
    ('pa', polar_align.polar_align,  'Refine Polar Alignment'),
    ('bl', backlash.backlash,        'Tune Backlash'),
    ('d',  config.scope.dump_status, 'Dump Status'),
    ('x',  sys.exit,                 'Exit'),
  ]

while True:

  for row in menu:
    print('%s.\t%s' % (row[0], row[2]))

  ans = input('Enter your selection -> ')

  for row in menu:
    if ans == row[0]:
      func = row[1]
      func()
