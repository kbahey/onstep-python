'''
Test parameters
'''
# To use over WiFi, change the following
HOST = '192.168.0.212'
PORT = '9999'

# Or, to use over USB
#HOST = ''
#PORT = '/dev/ttyUSB0'

# Location coordinates, change according to where you are
# Conestoga Lake Conservation Area
# lat = '+43*40'
# lon = '080:43'
lat = ''
lon = ''

# Offset from UTC, which is the opposite sign of the time zone
# Use +05 for EST/EDT
utc = '+05'

# Horizon and overhead limits
hor_lim = '-10'
ovh_lim = '90'

# Common stars, used the coordinates of one of them below
# Mothalah     '01:54:10' '+29*40:12'
# Beta Bootis  '15:01:56' '+40*23:25'
# Rasalhague   '17:34:56' '+12*33:31'
# Vega         '18:36:56' '+38*47:06'
# Deneb        '20:41:25' '+45*16:49'
# Eps Cygn     '20:46:13' '+33*58:19'
# Alpheratz    '23:04:45' '+15*12:18'
# Hamal        '02:07:11' '+23*27:42'
# Algol        '03:08:10' '+40*57:20'
# Aldebaran    '04:35:55' '+16*30:29'
# Menkalinan   '05:59:31' '+44*56:50'
# Alkaid       '13:47:32' '+49*18:48' # Circumpolar for most of northern latitudes
# Dubhe        '11:03:43' '+61*45:03'

# Coordinates
ra = '13:47:32'
de = '+49*18:48'


# Do not change anything below that line
import sys
import os
sys.path.append(os.getcwd())

import lx200.onstep as onstep
# Create a scope object
scope = onstep.onstep(host = HOST, port = PORT)
