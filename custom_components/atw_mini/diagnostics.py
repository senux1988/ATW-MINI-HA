"""Diagnostics support for ATW MINI."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import async_entries_for_config_entry
from homeassistant.components.diagnostics import async_redact_data

from .const import CONF_SCAN_INTERVAL, DOMAIN

TO_REDACT = {CONF_HOST, CONF_USERNAME, CONF_PASSWORD}


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: ConfigEntry
) -> dict:
    """Return diagnostics for a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    diagnostics = {
        "entry": {
            CONF_HOST: entry.data.get(CONF_HOST),
            CONF_USERNAME: entry.data.get(CONF_USERNAME),
            CONF_PASSWORD: "***redacted***" if entry.data.get(CONF_PASSWORD) else None,
            CONF_SCAN_INTERVAL: entry.options.get(
                CONF_SCAN_INTERVAL,
                entry.data.get(CONF_SCAN_INTERVAL),
            ),
        },
        "devices": [device.id for device in async_entries_for_config_entry(hass, entry.entry_id)],
        "data": coordinator.data.raw if coordinator.data else None,
    }
    return async_redact_data(diagnostics, TO_REDACT)
