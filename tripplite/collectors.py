#!/usr/bin/env python3

import logging
from typing import Dict, Optional

from tripplite.driver import Battery, battery_paths


LOG = logging.getLogger(__name__)


class Collector:
    battery: Optional[Battery] = None
    battery_path: str = ""

    def open_battery(self) -> None:
        if self.battery:
            return

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

    def get_data(self) -> Optional[Dict]:
        ups_data = None
        try:
            ups_data = self.battery.get()
        except OSError as ose:
            LOG.error(f"Unable to read from USB Serial for {self.battery_path}: {ose}")
            self.close_battery()
        return ups_data


if __name__ == "__main__":
    pass  # pragma: no cover
