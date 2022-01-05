# onstep-python
Python API for the [OnStep Telescope Controller](https://groups.io/g/onstep/wiki)

This API interfaces to OnStep, allowing scripting of test scenarios, actual telescope motion, ...etc..

Works over the following devices:
- USB serial
- WiFi (requires [OnStep's Smart Web Server](https://github.com/hjd1964/SmartWebServer))


Requires Python 3.x, and Python Serial.

Although this is written specifically for OnStep, it is mostly compatible with other telescope controllers
that use the [LX200 Command Protcol](http://www.skymtn.com/mapug-astronomy/ragreiner/LX200Commands.html).

## Configuration
Before using this API, you need to edit the examples/config.py.
A few required changes are needed in the examples/config.py:

a. How to connect to your controller? This can be over WiFi, or a serial USB port.
   Note that for FYSETC S6 the port is /dev/ttyACM0, and for the Blue Pill  and
   ESP32 controllers, the device name is /dev/ttyUSB0
b. The latitude and longitude (lat and lon)
c. The UTC offset (utc)

If you plan to use the WiFi instead of a serial USB cable, you need to change the HOST 
parameter in the config.py file.

## Quick Start
This method will present a menu for most of the example programs:

```
cd onstepy
./examples/menu.py
```

## Description
The following sample programs are provided. Adapt them to your own needs:

* init.py        - Sets coordinates, date, time, UTC offset, and starts tracking
* align.py       - This starts a 1-Star Alignment procedure (select the star's RA/DEC in config.py)
* home.py        - Return home
* slew.py        - Slew to a star
* slew_altaz.py  - Slew to an Alt/Az position
* drift_test.py  - Test if there is drift in RA (equatorial) and RA/DEC (Alt-Az)
* batch_align.py - Upload alignment points, with actual vs. instrument coordinates, and let OnStep do an alignment calculation
* stress-test.py - Repeatedly do slews west and east of the meridian, then wait for tracking then repeat. Useful to test thermal shutdown, mount accuracy ...etc.
* polar_align.py - Do a polar alignment using the :MP method (now present in the Android app)
* backlash.py    - Adjust the backlash on a terrestrial object
* report.py      - Report on an ongoing test

## Author
[Khalid Baheyeldin](https://baheyeldin.com)
