#!/usr/bin/env python3
"""Collector of metrics from TripLite battery backup for Prometheus."""

import argparse
import logging
import sys
import time
from socket import getfqdn
from typing import Generator, List


LOG = logging.getLogger(__name__)


try:
    from prometheus_client.core import GaugeMetricFamily, REGISTRY
    from prometheus_client import start_http_server
except ImportError as ie:
    LOG.error(
        f"prometheus_client not installed: {ie}. Please install with 'exporter' "
        "extra - e.g. `pip install tripplite[exporter]`"
    )
    sys.exit(1)
from tripplite.collectors import Collector


HOSTNAME = getfqdn()


class PrometheusCollector(Collector):
    """
    Prometheus Collector class.

    Get Dict from Battery and export Prometheus Guages via HTTP server.
    """

    key_prefix: str = "tripplite"
    labels: List[str] = ["hostname"]

    help_test = {
        "health": "UPS components health",
        "time_to_empty": "Runtime left in seconds",
    }

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
        """Collect metrics to expose for Prometheus."""
        start_time = time.time()
        LOG.info("Collection started")

        self.open_battery()
        ups_data = self.get_data()
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


def serve(args: argparse.Namespace) -> int:
    """Serve metrics for Prometheus to scrape."""
    start_http_server(args.port)
    REGISTRY.register(PrometheusCollector())
    LOG.info(f"Tripplite UPS Prometheus Exporter - listening on {args.port}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        LOG.info("Shutting down ...")
    return 0


if __name__ == "__main__":
    pass  # pragma: no cover
