"""
Python driver for TrippLite UPS battery backups.

Distributed under the GNU General Public License v2
Copyright (C) 2018 NuMat Technologies
"""
import argparse
import logging
import sys

from tripplite.driver import Battery, battery_paths


DEFAULT_PORT = 6969
LOG = logging.getLogger(__name__)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Read TrippLite devices.")
    parser.add_argument(
        "-d", "--debug", action="store_true", help="Verbose debug output"
    )
    parser.add_argument(
        "--exporter",
        choices=["json", "prometheus"],
        default="json",
        help="Format of data export [Default = json]",
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=DEFAULT_PORT,
        help=f"Port to run webserver on [Default = {DEFAULT_PORT}]",
    )
    return parser.parse_args()


def command_line() -> int:
    """Command line tool exposed through package install."""
    args = _parse_args()
    logging.basicConfig(
        format="[%(asctime)s] %(levelname)s: %(message)s (%(filename)s:%(lineno)d)",
        level=logging.DEBUG if args.debug else logging.INFO,
    )

    if not battery_paths:
        raise OSError("No TrippLite devices found.")

    if args.exporter == "json":
        import json
        output = []
        for path in battery_paths:
            with Battery(path) as battery:
                output.append(battery.get())
        if len(output) == 1:
            output = output[0]
        print(json.dumps(output, indent=4, sort_keys=True))

    elif args.exporter == "prometheus":
        import tripplite.prometheus
        return tripplite.prometheus.serve(args)

    return 0


if __name__ == '__main__':
    sys.exit(command_line())
