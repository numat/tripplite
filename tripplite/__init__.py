"""
Python driver for TrippLite UPS battery backups.

Distributed under the GNU General Public License v2
Copyright (C) 2018 NuMat Technologies
"""
from tripplite.driver import Battery, battery_paths


def command_line():
    """Command line tool exposed through package install."""
    import argparse
    import json

    argparse.ArgumentParser(description="Read TrippLite devices.")

    if not battery_paths:
        raise IOError("No TrippLite devices found.")
    output = []
    for path in battery_paths:
        with Battery(path) as battery:
            output.append(battery.get())
    if len(output) == 1:
        output = output[0]
    print(json.dumps(output, indent=4, sort_keys=True))


if __name__ == '__main__':
    command_line()
