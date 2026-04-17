"""Binary sensor platform for ATW MINI."""

from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .entity import AtwMiniCoordinatorEntity


@dataclass(frozen=True, kw_only=True)
class AtwMiniBinarySensorDescription(BinarySensorEntityDescription):
    """Describes an ATW MINI binary sensor."""

    value_key: str
    raw_tag: str


BINARY_SENSOR_DESCRIPTIONS: tuple[AtwMiniBinarySensorDescription, ...] = (
    AtwMiniBinarySensorDescription(
        key="heat_pump_enabled",
        translation_key="heat_pump_enabled",
        name="Heat pump enabled",
        value_key="heat_pump_enabled",
        raw_tag="control_st1",
        icon="mdi:power",
    ),
    AtwMiniBinarySensorDescription(
        key="defrost",
        translation_key="defrost",
        name="Defrost",
        value_key="operation_state",
        raw_tag="status_st1",
        icon="mdi:snowflake-melt",
    ),
    AtwMiniBinarySensorDescription(
        key="heat_pump_running",
        translation_key="heat_pump_running",
        name="Heat pump running",
        value_key="heat_pump_running",
        raw_tag="status_st2",
        icon="mdi:fan",
    ),
    AtwMiniBinarySensorDescription(
        key="time_setback_active",
        translation_key="time_setback_active",
        name="Time setback active",
        value_key="time_setback_active",
        raw_tag="status_st4",
        icon="mdi:timer-sand",
    ),
    AtwMiniBinarySensorDescription(
        key="hdo_blocking_active",
        translation_key="hdo_blocking_active",
        name="HDO blocking active",
        value_key="hdo_blocking_active",
        raw_tag="status_st5",
        icon="mdi:cancel",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up ATW MINI binary sensors."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        AtwMiniBinarySensor(coordinator, description)
        for description in BINARY_SENSOR_DESCRIPTIONS
    )


class AtwMiniBinarySensor(AtwMiniCoordinatorEntity, BinarySensorEntity):
    """Representation of an ATW MINI binary sensor."""

    entity_description: AtwMiniBinarySensorDescription

    def __init__(self, coordinator, description: AtwMiniBinarySensorDescription) -> None:
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = (
            f"{coordinator.config_entry.entry_id}_{self.entity_description.key}"
        )

    @property
    def is_on(self) -> bool | None:
        """Return the binary sensor state."""
        if self.coordinator.data is None:
            return None
        value = self.coordinator.data.values.get(self.entity_description.value_key)
        if self.entity_description.key == "defrost":
            return value == "defrost"
        return value

    @property
    def extra_state_attributes(self) -> dict[str, str | bool | None]:
        """Return extra state attributes."""
        return {
            "raw_tag": self.entity_description.raw_tag,
            "last_update_success": self.coordinator.last_update_success,
            "raw_value": self.coordinator.data.raw.get(self.entity_description.raw_tag)
            if self.coordinator.data
            else None,
        }
