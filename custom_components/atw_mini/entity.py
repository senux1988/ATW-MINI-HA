"""Base entity for ATW MINI entities."""

from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, MANUFACTURER, MODEL
from .coordinator import AtwMiniDataUpdateCoordinator


class AtwMiniCoordinatorEntity(CoordinatorEntity[AtwMiniDataUpdateCoordinator]):
    """Base class for all ATW MINI coordinator entities."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: AtwMiniDataUpdateCoordinator) -> None:
        super().__init__(coordinator)
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.config_entry.entry_id)},
            manufacturer=MANUFACTURER,
            model=MODEL,
            name=coordinator.config_entry.title,
            configuration_url=coordinator.api.status_url,
        )

