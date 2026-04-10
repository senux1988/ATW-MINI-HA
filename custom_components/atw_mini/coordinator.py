"""Data coordinator for the ATW MINI integration."""

from __future__ import annotations

from datetime import timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import AtwMiniApiClient, AtwMiniApiConnectionError, AtwMiniApiParseError
from .const import CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL, DOMAIN
from .parser import AtwMiniStatus

LOGGER = logging.getLogger(__name__)


class AtwMiniDataUpdateCoordinator(DataUpdateCoordinator[AtwMiniStatus]):
    """Coordinate ATW MINI data updates."""

    config_entry: ConfigEntry

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        self.config_entry = entry
        self.api = AtwMiniApiClient(
            session=async_get_clientsession(hass),
            host=entry.data[CONF_HOST],
            username=entry.data[CONF_USERNAME],
            password=entry.data[CONF_PASSWORD],
        )

        update_interval = timedelta(
            seconds=entry.options.get(
                CONF_SCAN_INTERVAL,
                entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL),
            )
        )

        super().__init__(
            hass,
            logger=LOGGER,
            name=f"{DOMAIN}_{entry.title}",
            update_interval=update_interval,
        )

    async def _async_update_data(self) -> AtwMiniStatus:
        """Fetch data from the device."""
        try:
            return await self.api.async_get_status()
        except (AtwMiniApiConnectionError, AtwMiniApiParseError) as err:
            raise UpdateFailed(str(err)) from err
