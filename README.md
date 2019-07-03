# onstep-python
A Python API for the OnStep Telescope Controller, LX200 compatible

Allows scripting of test scenarios, actual telescope motion, ...etc..

Requires Python3, and Python Serial.

Although this is written specifically for OnStep, it is mostly compatible with other LX200
telescopes, and can easily be adaptable to them. 

## Configuration
Before using this API, you need to edit the examples/config.py. Change the
date/time, UTC offset, Latitude, Longitude, and the HOST IP address of your OnStep's WiFi.

## Quick Start
This method will present a menu of available programs:

```
cd onstepy
./examples/menu.py
```

## Description
The following sample programs are provided. Adapt them to your own needs:

* init.py        - This enables tracking
* align.py       - This starts a 1-Star Alignment procedure (select its RA/DEC in config.py)
* home.py        - Return home
* slew.py        - Slew to a star
* backlash.py    - Adjust the backlash on a terrestrial object
* polar_align.py - Do a polar alignment using the :MP method
* drift_test.py  - Test if there is drift in RA (equatorial) and RA/DEC (Alt-Az)
* mon.py         - Monitor an ongoing test
* report.py      - Report on an ongoing test
* batch_align.py - Upload alignment points, with actual vs. instrument coordinates, and let
                 OnStep do an alignment calculation
* stress-test.py - Repeatedly do slews west and east of the meridian, then wait for tracking
                 then repeat. Useful to test thermal shutdown, mount accuracy ...etc.

## Author
(https://baheyeldin.com)[Khalid Baheyeldin]
