# OnStep Telescope Controller interface

import lx200.tty
import lx200.sock
import time
from datetime import datetime

class onstep:
  def __init__(self, port = '', host = ''):
    self.host = host
    self.port = port

    # Check what mode we are in, serial USB or over TCP/IP
    if self.host == '' and self.port != '':
      self.scope = lx200.tty.tty(port=self.port)
      self.scope.open()
    else:
      if port.isnumeric():
        self.scope = lx200.sock.sock()
        self.scope.connect(self.host, int(self.port))
      else:
        raise NonNumericPort

    self.is_slewing = False
    self.is_tracking = False
    self.is_parked = None
    self.type = None
    self.home_wait = False
    self.is_home = None
    self.pier_side = None
    self.pec_recorded = False
    self.pec = None
    self.pps = False
    self.pulse_guide_rate = None
    self.guide_rate = None
    self.general_error = None

    # TODO Need to add variables for:
    # - aligned or not
    # - number of stars aligned

    self.last_update = datetime.now()

  def close(self):
    self.scope.close()

  # Keep receiving from the port, until you get a terminating #
  def recv_message(self):
    s = self.scope.recv()
    while len(s) > 0 and s[-1] != '#':
      s += self.scope.recv()
    return s[:-1]

  def get_tracking_rate(self):
    self.scope.send('#:GT#')
    return self.recv_message()

  def set_send_wait(self, wait):
    lx200.tty.send_wait = wait

  def align(self, num_stars = 1):
    # Align command
    self.scope.send('#:A' + str(num_stars) + '#')
    return self.scope.recv()

  def get_align_status(self):
    # Align command
    self.scope.send('#:A?#')
    return self.recv_message()

  def tracking_on(self):
    # Turn on tracking
    self.scope.send('#:Te#')
    return self.scope.recv()

  def tracking_off(self):
    # Turn off tracking
    self.scope.send('#:Td#')
    return self.scope.recv()

  def send_str(self, string):
    # Send a string
    self.scope.send(string)
    return self.scope.recv()

  def dump_status(self):
    self.update_status()
    print('Mount type:       ' + str(self.type))
    print('Slewing:          ' + str(self.is_slewing))
    print('Tracking:         ' + str(self.is_tracking))
    print('Parking:          ' + str(self.is_parked))
    print('Home:             ' + str(self.is_home))
    print('Wait Home:        ' + str(self.home_wait))
    print('Pier-side:        ' + str(self.pier_side))
    print('PEC Recorded?:    ' + str(self.pec_recorded))
    print('PEC:              ' + str(self.pec))
    print('PPS:              ' + str(self.pps))
    print('Pulse guide rate: ' + str(self.pulse_guide_rate))
    print('Guide rate:       ' + str(self.guide_rate))
    print('General error:    ' + str(self.general_error))

  def update_status(self):
    now = datetime.now()

    self.last_update = now

    self.scope.send(':GU#')
    s = self.recv_message()

    if 'n' in s and 'N' in s:
      self.is_slewing = False
      self.is_tracking = False

    if not 'n' in s and not 'N' in s:
      self.is_slewing = True
      self.is_tracking = False

    if not 'n' in s and 'N' in s:
      self.is_slewing = False
      self.is_tracking = True

    if 'n' in s and not 'N' in s:
      self.is_slewing = True
      self.is_tracking = False

    if 'p' in s:
      self.is_parked = False
    if 'P' in s:
      self.is_parked = True
    if 'I' in s:
      self.is_parked = 'Parking in progress'
    if 'F' in s:
      self.is_parked = 'Parking failed'

    if 'H' in s:
      self.is_home = True
    else:
      self.is_home = False

    if 'w' in s:
      self.home_wait = True

    if 'G' in s:
      self.guide = 'Guide pulse active'

    if 'S' in s:
      self.pps = True
    else:
      self.pps = False

    if 'R' in s:
      self.pec_recorded = True
    else:
      self.pec_recorded = False

    if '/' in s:
      self.pec = 'Ignore'
    if ',' in s:
      self.pec = 'Ready to Play'
    if '~' in s:
      self.pec = 'Playing'
    if ';' in s:
      self.pec = 'Ready to Record'
    if '^' in s:
      self.pec = 'Recording'

    if 'E' in s:
      self.type = 'Equatorial'
    if 'K' in s:
      self.type = 'Fork'
    if 'k' in s:
      self.type = 'Fork Alternate'
    if 'A' in s:
      self.type = 'AltAz'

    if 'o' in s:
      self.pier_side = 'None'
    if 'T' in s:
      self.pier_side = 'East'
    if 'W' in s:
      self.pier_side = 'West'

    if len(s) > 3:
      self.pulse_guide_rate = s[-3]
      self.guide_rate = s[-2]
      self.general_error = ord(s[-1])-ord('0')

  def set_target_azm(self, azm):
    self.scope.send(':Sz' + azm + '#')
    return self.scope.recv()

  def set_target_alt(self, alt):
    self.scope.send(':Sa' + alt + '#')
    return self.scope.recv()

  def set_target_ra(self, ra):
    self.scope.send(':Sr' + ra + '#')
    return self.scope.recv()

  def set_target_de(self, de):
    self.scope.send(':Sd' + de + '#')
    return self.scope.recv()

  def slew_equ(self):
    # Slew to a certain RA and DEC
    self.scope.send(':MS#')
    rc = self.scope.recv()
    if rc == '0':
      return rc, 'Goto is possible'
    elif rc == '1': 
      return rc, 'below the horizon limit'
    elif rc == '2':
      return rc, 'above overhead limit'
    elif rc == '3':
      return rc, 'controller in standby'
    elif rc == '4':
      return rc, 'mount is parked'
    elif rc == '5':
      return rc, 'Goto in progress'
    elif rc == '6':
      return rc, 'outside limits (MaxDec, MinDec, UnderPoleLimit, MeridianLimit)'
    elif rc == '7':
      return rc, 'hardware fault'
    elif rc == '8':
      return rc, 'already in motion'
    else:
      return rc, 'unspecified error'

    return rc

  def slew_hor(self):
    # Slew to a certain Alt and Azm
    self.scope.send(':MA#')
    rc = self.scope.recv()
    if rc == '0':
      return rc, 'Goto is possible'
    elif rc == '1': 
      return rc, 'below the horizon limit'
    elif rc == '2':
      return rc, 'above overhead limit'
    elif rc == '3':
      return rc, 'controller in standby'
    elif rc == '4':
      return rc, 'mount is parked'
    elif rc == '5':
      return rc, 'Goto in progress'
    elif rc == '6':
      return rc, 'outside limits (MaxDec, MinDec, UnderPoleLimit, MeridianLimit)'
    elif rc == '7':
      return rc, 'hardware fault'
    elif rc == '8':
      return rc, 'already in motion'
    else:
      return rc, 'unspecified error'

    return rc

  def slew_polar(self):
    # Slew to the assumed position for polar alignment
    self.scope.send(':MP#')
    rc = self.scope.recv()
    if rc == '0':
      return rc, 'Goto is possible'
    elif rc == '1': 
      return rc, 'below the horizon limit'
    elif rc == '2':
      return rc, 'above overhead limit'
    elif rc == '3':
      return rc, 'controller in standby'
    elif rc == '4':
      return rc, 'mount is parked'
    elif rc == '5':
      return rc, 'Goto in progress'
    elif rc == '6':
      return rc, 'outside limits (MaxDec, MinDec, UnderPoleLimit, MeridianLimit)'
    elif rc == '7':
      return rc, 'hardware fault'
    elif rc == '8':
      return rc, 'already in motion'
    else:
      return rc, 'unspecified error'

    return rc

  def sync(self):
    # Move back to home position
    self.update_status()
    # Sync only if the scope is tracking
    if self.is_tracking == True:
      self.scope.send(':CM#')

  def set_backlash(self, axis = 1, value = 0):
    # Set backlash for axis
    if axis == 1:
      ax = 'R'
    elif axis == 2:
      ax = 'D'
    else:
      return '0'

    self.scope.send(':$B' + ax + str(value) + '#')
    return self.scope.recv()

  def get_backlash(self, axis = 1):
    # Get backlash for axis
    if axis == 1:
      ax = 'R'
    elif axis == 2:
      ax = 'D'
    else:
      return '0'

    self.scope.send(':%B' + str(ax) + '#')
    return self.recv_message()

  def get_debug_equ(self):
    # Get Equatorial values in decimal 
    self.scope.send(':GXFE#')
    return self.recv_message()

  def get_ax_motor_pos(self, axis = 1):
    # Get Axis motor position
    if axis == 1:
      ax = '8'
    elif axis == 2:
      ax = '9'
    else:
      return '0'

    self.scope.send(':GXF' + str(ax) + '#')
    return self.recv_message()

  def get_spd(self, axis = 1):
    # Get Axis motor position
    if axis == 1:
      ax = '4'
    elif axis == 2:
      ax = '5'
    else:
      return '0'

    self.scope.send(':GXE' + str(ax) + '#')
    return self.recv_message()

  def get_cor_alt(self):
    # Get Altitude Correction
    self.scope.send(':GX02#')
    return self.recv_message()

  def get_cor_azm(self):
    # Get Azimuth Correction
    self.scope.send(':GX03#')
    return self.recv_message()

  def get_cor_do(self):
    # Get Cone Error Correction
    self.scope.send(':GX04#')
    return self.recv_message()

  def set_utc_offset(self, utc_offset):
    print('Setting UTC Offset to: ' + utc_offset)
    self.scope.send(':SG' + utc_offset + '#')
    time.sleep(1)
    ret = self.scope.recv()
    if ret == '1':
      return True
    else:
      return False

  def get_utc(self):
    # Get controller utc offset
    self.scope.send(':GG#')
    return self.recv_message()

  def set_date(self):
    t = datetime.now()
    date = t.strftime("%m/%d/%y")
    print('Setting date to: ' + date)
    self.scope.send('#:SC' + date + '#')
    time.sleep(4)
    ret = self.scope.recv()
    if ret == '1':
      return True
    else:
      return False

  def set_utcdate(self):
    t = datetime.utcnow()
    date = t.strftime("%m/%d/%y")
    print('Setting date to: ' + date)
    self.scope.send(':SC' + date + '#')
    time.sleep(4)
    ret = self.scope.recv()
    if ret == '1':
      return True
    else:
      return False

  def get_date(self):
    # Get controller date
    self.scope.send(':GC#')
    return self.recv_message()

  def set_time(self):
    t = datetime.now()
    curr_time = t.strftime('%H:%M:%S')
    print('Setting time to: ' + curr_time)
    self.scope.send(':SL' + curr_time + '#')
    time.sleep(3)
    ret = self.scope.recv()
    if ret == '1':
      return True
    else:
      return False

  def set_utctime(self):
    t = datetime.utcnow()
    curr_time = t.strftime('%H:%M:%S')
    print('Setting time to: ' + curr_time)
    self.scope.send(':SL' + curr_time + '#')
    time.sleep(3)
    ret = self.scope.recv()
    if ret == '1':
      return True
    else:
      return False

  def get_time(self, high_precision = False):
    # Get controller time
    if high_precision == True:
      cmd = 'GLa'
    else:
      cmd = 'GL'
    self.scope.send(':' + cmd + '#')
    return self.recv_message()

  def get_sidereal_time(self, high_precision = False):
    # Get controller sidereal time
    if high_precision == True:
      cmd = 'GSa'
    else:
      cmd = 'GS'
    self.scope.send(':' + cmd + '#')
    return self.recv_message()

  def set_horizon_limit(self, limit):
    self.scope.send(':Sh' + limit + '#')
    time.sleep(1)
    ret = self.scope.recv()
    if ret == '1':
      return True
    else:
      return False

  def set_overhead_limit(self, limit):
    self.scope.send(':So' + limit + '#')
    time.sleep(1)
    ret = self.scope.recv()
    if ret == '1':
      return True
    else:
      return False

  def set_longitude(self, longitude):
    print('Setting longitude to: ' + longitude)
    self.scope.send(':Sg' + longitude + '#')
    time.sleep(2)
    ret = self.scope.recv()
    if ret == '1':
      return True
    else:
      return False

  def get_longitude(self):
    # Get controller utc offset
    self.scope.send(':Gg#')
    return self.recv_message()

  def set_latitude(self, latitude):
    print('Setting latitude to: ' + latitude)
    self.scope.send(':St' + latitude + '#')
    time.sleep(2)
    ret = self.scope.recv()
    if ret == '1':
      return True
    else:
      return False

  def get_latitude(self):
    # Get controller utc offset
    self.scope.send(':Gt#')
    return self.recv_message()

  def get_version(self):
    # Get OnStep version
    self.scope.send('#:GVN#')
    return self.recv_message()

  def get_ra(self, high_precision = False):
    # Get RA
    if high_precision == True:
      cmd = 'GRa'
    else:
      cmd = 'GR'
    self.update_status()
    self.scope.send(':' + cmd + '#')
    return self.recv_message()

  def get_de(self):
    cmd = 'GD'
    self.update_status()
    self.scope.send(':' + cmd + '#')
    return self.recv_message()

  def get_alt(self):
    # Get Alt
    self.update_status()
    self.scope.send(':GA#')
    return self.recv_message()

  def get_azm(self):
    # Get Azm
    self.update_status()
    self.scope.send(':GZ#')
    return self.recv_message()

  def return_home(self):
    # Move back to home position
    self.update_status()
    self.scope.send(':hC#')

  def reset_home(self):
    # Reset, as if pointing to the home position
    self.update_status()
    self.scope.send(':hF#')

  def set_speed(self, speed = '20x'):
    # Set speed
    if   speed == '0.25x':
      s = '0'
    elif speed == '0.5x':
      s = '1'
    elif speed == '1x':
      s = 'G'
    elif speed == '2x':
      s = '3'
    elif speed == '4x':
      s = '4'
    elif speed == '8x':
      s = 'C'
    elif speed == '20x':
      s = 'M'
    elif speed == '48x':
      s = 'F'
    elif speed == 'half':
      s = 'S'
    elif speed == 'max':
      s = '9'
    else:
      return False

    self.scope.send(':R' + s + '#')
    return True

  def stop(self):
    # Stop all movememnt
    self.scope.send(':Q#')

  def move(self, direction = ''):
    # Move in a certain direction
    if direction == 'n' or direction == 's' or direction == 'w' or direction == 'e':
      self.scope.send(':M' + direction + '#')
      return True
    else:
      return False

