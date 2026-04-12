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
        key="defrost",
        translation_key="defrost",
        name="Defrost",
        value_key="st1",
        raw_tag="st1",
        icon="mdi:snowflake-melt",
    ),
    AtwMiniBinarySensorDescription(
        key="status_2",
        translation_key="status_2",
        name="Status 2",
        value_key="st2",
        raw_tag="st2",
    ),
    AtwMiniBinarySensorDescription(
        key="status_3",
        translation_key="status_3",
        name="Status 3",
        value_key="st3",
        raw_tag="st3",
    ),
    AtwMiniBinarySensorDescription(
        key="status_4",
        translation_key="status_4",
        name="Status 4",
        value_key="st4",
        raw_tag="st4",
    ),
    AtwMiniBinarySensorDescription(
        key="status_5",
        translation_key="status_5",
        name="Status 5",
        value_key="st5",
        raw_tag="st5",
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
