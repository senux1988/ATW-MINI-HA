"""Constants for the ATW MINI integration."""

from __future__ import annotations

from datetime import timedelta

DOMAIN = "atw_mini"
MANUFACTURER = "ATW MINI / NeoRe Mini"
MODEL = "ATW MINI"
DEFAULT_NAME = "ATW MINI"
CONF_DEFAULT_USERNAME = "admin"
DEFAULT_SCAN_INTERVAL = 30
DEFAULT_TIMEOUT = 10

CONF_SCAN_INTERVAL = "scan_interval"

PLATFORMS = ("sensor", "binary_sensor")

UPDATE_INTERVAL = timedelta(seconds=DEFAULT_SCAN_INTERVAL)
