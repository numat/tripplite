"""Driver for TrippLite UPS battery backups."""
import hid

vendor_id = 0x09ae

# These change on each call to `hid.enumerate` so must be cached.
battery_paths = [
    device['path'].decode()
    for device in hid.enumerate()
    if device['vendor_id'] == vendor_id
]

structure = {
    'config': {
        'voltage': {
            'address': 48,
            'bytes': 1,
            'format': 'i'
        },
        'frequency': {
            'address': 2,
            'bytes': 1,
            'format': 'i'
        },
        'power': {
            'address': 3,
            'bytes': 2,
            'format': 'i'
        }
    },
    'status': {
        'address': 50,
        'bytes': 1,
        'format': 'b',
        'keys': [
            'shutdown imminent',
            'ac present',
            'charging',
            'discharging',
            'needs replacement',
            'below remaining capacity',
            'fully charged',
            'fully discharged'
        ]
    },
    'input': {
        'voltage': {
            'address': 24,
            'bytes': 2,
            'format': 'f'
        },
        'frequency': {
            'address': 25,
            'bytes': 2,
            'format': 'f'
        }
    },
    'output': {
        'voltage': {
            'address': 27,
            'bytes': 2,
            'format': 'f'
        },
        'power': {
            'address': 71,
            'bytes': 2,
            'format': 'i'
        }
    },
    'health': {
        'address': 52,
        'bytes': 1,
        'format': 'i'
    },
    'time to empty': {
        'address': 53,
        'bytes': 2,
        'format': 'i'
    }
}


class Battery:
    """Driver for TrippLite UPS battery backups."""

    def __init__(self, path=None):
        """Connect to the device.

        Args:
            path (Optional): The HID path of the device. Only needed if
            reading multiple devices.

        """
        self.device = hid.device()
        if not battery_paths:
            raise OSError("Could not find any connected TrippLite devices.")
        if path is not None and path not in battery_paths:
            raise ValueError(f"Path {path} not in {', '.join(battery_paths)}.")
        self.path = path or battery_paths[0]

    def __enter__(self):
        """Provide entrance to context manager."""
        self.open()
        return self

    def __exit__(self, *args):
        """Provide exit to context manager."""
        self.close()

    def open(self):
        """Open connection to the device."""
        self.device.open_path(self.path.encode())

    def close(self):
        """Close connection to the device."""
        self.device.close()

    def get(self):
        """Return an object containing all available data."""
        output = {}
        output['device_id'] = self.path
        for category, data in structure.items():
            if 'address' in data:
                output[category] = self._read(data)
            else:
                output[category] = {}
                for subcategory, options in data.items():
                    output[category][subcategory] = self._read(options)
        return output

    def _read(self, options, retries=3):
        """Read a HID report from the TrippLite connection.

        This reads binary, one-byte ints, two-byte ints (little-endian),
        and floats (little-endian two-byte ints, divided by 10). See the
        TrippLite communication interface manual for more.
        """
        report = self.device.get_feature_report(options['address'],
                                                options['bytes'] + 1)
        if not report:
            if retries > 0:
                return self._read(options, retries - 1)
            raise OSError("Did not receive data.")
        if options['address'] != report[0]:
            raise OSError("Received unexpected data.")
        if options['format'] == 'b':
            bits = f'{report[1]:08b}'[::-1]
            return {k: bool(int(v)) for k, v in zip(options['keys'], bits)}
        elif options['format'] == 'i' and options['bytes'] == 2:
            return (report[2] << 8) + report[1]
        elif options['format'] == 'i' and options['bytes'] == 1:
            return report[1]
        elif options['format'] == 'f':
            return ((report[2] << 8) + report[1]) / 10.0
