tripplite
=========

Python USB interface and command-line tool for TrippLite UPS battery backups.

![](https://www.markertek.com/productImage/450X450/SMART1500LCD.JPG)

Background
==========

TrippLite offers [UI software](https://www.tripplite.com/products/power-alert)
for monitoring its batteries. However, most of its batteries don't have
network access, and the existing TrippLite software requires a local install.

I wanted to monitor the UPS from a remote headless Linux server, so I wrote
this tool.

Installation
============

```
apt install gcc libusb-1.0-0-dev libudev-dev
pip install tripplite
```

Connect a USB cable from the UPS to your headless server, and you should be
ready to run. If you don't want to run as root, see *Note on Permissions*
below.

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

To use in shell scripts, parse the json output with something like
[jq](https://stedolan.github.io/jq/). For example,
`tripplite | jq '.status."ac present"` will return whether or not the unit
detects AC power.

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
`state['status']['ac present']` and `state['status']['shutdown imminent']` for
alerts, and consider logging voltage, frequency, and power.

Note on Permissions
===================

To read the TrippLite, you need access to the USB port. You have options:

 * Run everything as root
 * Add your user to the `dialout` group to access *all* serial ports
 * Create a group restricted to accessing TrippLite USB devices through `udev`

For the last option, the rule looks like:

```
echo 'SUBSYSTEM=="usb", ATTRS{idVendor}=="09ae", GROUP="tripplite"' > /etc/udev/rules.d/tripplite.rules
udevadm control --reload-rules
```
