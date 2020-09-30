#!/usr/bin/env python3

import argparse
import logging
import sys
import time
from socket import getfqdn
from typing import Dict, Generator, List, Optional

from prometheus_client.core import GaugeMetricFamily, REGISTRY
from prometheus_client import start_http_server
from tripplite.driver import Battery, battery_paths


DEFAULT_PORT = 6969
HOSTNAME = getfqdn()
LOG = logging.getLogger(__name__)


class TrippliteCollector:
    key_prefix: str = "tripplite"
    labels: List[str] = ["hostname"]
    battery: Optional[Battery] = None
    battery_path: str = ""

    help_test = {
        "health": "UPS components health",
        "time_to_empty": "Runtime left in seconds",
    }

    def open_battery(self) -> None:
        if not battery_paths:
            LOG.error("No Tripplite battery found")
            return None
        self.battery_path = battery_paths[0]
        self.battery = Battery(self.battery_path)
        self.battery.open()
        LOG.info(f"Connected to {self.battery_path} battery")

    def close_battery(self) -> None:
        self.battery.close()
        LOG.info(f"Disconnecting {self.battery_path} battery to try reconnect")
        self.battery = None
        self.battery_path = ""

    def _handle_counter(self, category: str, value: float) -> GaugeMetricFamily:
        normalized_category = category.replace(" ", "_")
        key = f"{self.key_prefix}_{normalized_category}"
        g = GaugeMetricFamily(
            key,
            self.help_test.get(normalized_category, "Tripplite Metric"),
            labels=self.labels,
        )
        g.add_metric([HOSTNAME], value)
        return g

    def collect(self) -> Generator[GaugeMetricFamily, None, None]:
        start_time = time.time()
        LOG.info("Collection started")

        if not self.battery:
            self.open_battery()
            if not self.battery:
                sys.exit(2)

        ups_data = None
        try:
            ups_data = self.battery.get()
        except OSError as ose:
            LOG.error(f"Unable to read from USB Serial for {self.battery_path}: {ose}")
            self.close_battery()

        if not ups_data:
            return

        for category, value in ups_data.items():
            if isinstance(value, int):
                yield self._handle_counter(category, value)
            else:
                for subcategory, subvalue in value.items():
                    combined_category = f"{category}_{subcategory}"
                    yield self._handle_counter(combined_category, float(subvalue))

        run_time = time.time() - start_time
        LOG.info(f"Collection finished in {run_time}s")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", "--debug", action="store_true", help="Verbose debug output"
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=DEFAULT_PORT,
        help=f"Port to run webserver on [DEFAULT = {DEFAULT_PORT}]",
    )
    args = parser.parse_args()
    logging.basicConfig(
        format="[%(asctime)s] %(levelname)s: %(message)s (%(filename)s:%(lineno)d)",
        level=logging.DEBUG if args.debug else logging.INFO,
    )

    start_http_server(args.port)
    REGISTRY.register(TrippliteCollector())
    LOG.info(f"Tripplite UPS Monitoring - listening on {args.port}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        LOG.info("Shutting down ...")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
