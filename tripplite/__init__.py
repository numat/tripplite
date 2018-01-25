"""
Python driver for TrippLite UPS battery backups.

Distributed under the GNU General Public License v2
Copyright (C) 2018 NuMat Technologies
"""
from tripplite.driver import Battery


def command_line():
    """Command line tool exposed through package install."""
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Read TrippLite status.")
    parser.add_argument('-p', '--product_id', type=int, default=None,
                        help="The TrippLite UPS HID product idea. Only needed "
                        "if multiple TrippLite devices are connected.")
    args = parser.parse_args()
    battery = Battery(args.product_id)
    print(json.dumps(battery.get(), indent=4, sort_keys=True))
    battery.close()


if __name__ == '__main__':
    command_line()
