tripplite
=========

Python USB interface and command-line tool for TrippLite UPS battery backups.

![](https://www.markertek.com/productImage/450X450/SMART1500LCD.JPG)

Background
==========

TrippLite offers [UI software](https://www.tripplite.com/products/power-alert)
for monitoring its batteries. However, most of its batteries only have USB,
and the only existing TrippLite software requires a local install.

I wanted to monitor battery health from a remote headless Linux server, so I
wrote this driver.

Installation
============

```
sudo apt install gcc libusb-1.0-0-dev libudev-dev
pip install hidapi
```

Connect a USB cable from the UPS to your headless server, and you should be
ready to run.

Command Line
============

```
$ tripplite
{
    "config": {
        "frequency": 60,  # Hz
        "power": 1500,  # VA
        "voltage": 120  # V
    },
    "health": 100,  # %
    "input": {
        "frequency": 59.7,  # Hz
        "voltage": 117.2  # V
    },
    "output": {
        "power": 324,  # W
        "voltage": 117.2  # V
    },
    "status": {
        "ac present": true,
        "below remaining capacity": true,
        "charging": false,
        "discharging": false,
        "fully charged": true,
        "fully discharged": false,
        "needs replacement": false,
        "shutdown imminent": false
    },
    "time to empty": 1004  # s
}
```

If you have multiple TrippLite devices connected to the server, you'll need to
specify a product id (findable on `lsusb`). See `tripplite --help` for more.

Combine with a CLI JSON parser for basic shell scripts.

Python
======

If you'd like to link this to more complex behavior (e.g. data logging,
text alerts), consider using a Python script.

```python
from tripplite import Battery
battery = Battery()
state = battery.get()
battery.close()
```

The `state` variable will contain an object with the same format as above. Use
`state['status']['discharging']` and `state['status']['shutdown imminent']` for
alerts, and consider logging voltage, frequency, and power.
